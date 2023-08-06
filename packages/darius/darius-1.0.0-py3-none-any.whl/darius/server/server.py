# < - Package Imports
from ..client_side import status
from ..Parsing.http import (ParseHeaders,ParseHTTP,AwaitFullBody\
,replace,AppendHeaders,AppendRawHeaders)
from ..Parsing import websocket
from .routes import SocketView

# < - Server Hadnling
import socket
import threading

# < - For Parsing - Hints
from datetime import datetime
import re
from typing import Any,Union
from traceback import print_exception

# < - File handling-Decoding
from os.path import getsize,join
from urllib.request import unquote

# < - Websocket handling functions
SocketBin : callable;SocketBinSend : callable
SocketBin,SocketBinSend = websocket.ReceiveData,websocket.SendData
DataWait : callable = websocket.AwaitSocketData 
EnsureSocket : callable = websocket.EnsureSocket

def lazy_read(file): #Function to lazy read
    while True:
        data = file.read(1024)
        if not data:
            break
        yield data

LOCALHOST : str = "127.0.0.1"
HTTP_PORT : int = 80
STANDAR_404_PAGE : callable = lambda page : "<b>Page {} Was not Found (404 Status Code)</b>".format(page)
STANDAR_500_PAGE : str = "<h1>500 Internal Server Error</h1>"
CORS : callable = lambda origin : 'Access-Control-Allow-Origin : {}\r\n'.format(origin)
X_FRAME : callable = lambda value : f'X-Frame-Options: {value}\r\n'

class HttpServer:
    """
    A Standar Hyper Text Transfer Protool (HTTP) server,\n
    that given a HTTP request on a specific route,\n
    returns a specific 'View' class method depending on the method\n
    and the PATH, which if not found a 404 page is returned passed in the context of:\n
    param: page404 : callable = STANDAR_404_PAGE
        STANDAR_404_PAGE = lambda page : '<b>Page {} Was not Found (404 Status Code)</b>'.format(page)

    if an Exception is raised in one of the passed in VIEWS the standar 500 Page will be passed in
        param: page505 : str = STANDAR_500_PAGE 
    """

    def __init__(self,host : str = LOCALHOST,receive_size : int = 1024,port : int = HTTP_PORT,page404 : callable = STANDAR_404_PAGE,page500 : str = STANDAR_500_PAGE,CORS_DOMAINS : list = [],**kwargs):
        isHttp = kwargs.get('http')
        print(f"Initiliazing local {'HTTP' if isHttp is None else 'WS' if isHttp.strip().lower() != 'standar server' else 'HTTP & WS'} Server on {host}:{port}")
        self.adress : tuple = (host,port)
        self.connection : socket.socket = socket.socket()
        try:
            self.connection.bind(self.adress)
        except:
            raise RuntimeError(f"Could not bind.Something else is running on {self.adress[0]}:{self.adress[1]}.")
        self.urls : dict = kwargs.get("URLS")

        if(self.urls is None or type(self.urls) != dict):
            raise ValueError("URLS were of type {}, when they should have been {}.".format(type(self.urls),dict))

        self.page404 : callable = page404 
        self.page500 : str = page500
        self.receive_size = receive_size
        assert type(CORS_DOMAINS) == list
        self.cors = self.CORS_DOMAINS = CORS_DOMAINS
        self.xframe =  X_FRAME('SAMEORIGIN')

        if '*' in self.cors: #Everything is allowed
            self.cors = lambda _: CORS('*')
            tmp = '*'
        
        elif None in self.cors: #No Cors means it is automatically disallowed
            self.cors = lambda _: ''
            tmp = 'None (Only same site)'
        
        else:
            self.cors = lambda domain : CORS(domain) if domain in self.CORS_DOMAINS else ''
            tmp = f'{len(CORS_DOMAINS)} Domains'

        print(f"(HTTP) Configured CORS Allowed Origins as {tmp}.")

        del isHttp

    def HandleCORS(self,msg,headers):
        isAllowed = headers[0].get("Origin")
        if isAllowed:
            origin = isAllowed
            msg = AppendRawHeaders(msg,b"\r\n" + self.cors(origin).encode())
        msg = AppendRawHeaders(msg,b"\r\n" + self.xframe.encode())
        return msg

    def ParseBody(self,body,client,headers):
        client.settimeout(4)
        body = AwaitFullBody(headers,body,lambda : client.recv(self.receive_size))
        client.settimeout(None)
        headers = headers,body
        return headers

    def handleHTTP(self,client : socket.socket,headers : dict,URLS : dict,**kwargs) -> None:
        hasBodyParsed : bool = type(headers) in (tuple,list) #See if there is form data
        target = headers[0]["method"].split(" ")[1] if hasBodyParsed else headers["method"].split(" ")[1] #target route
        
        # Loop through the urls and try to find it
        for url in URLS:
            match = re.fullmatch(url,target) #full regex match
            if match: 
                try:
                    # Only if the path is found wait for the full fucking request
                    if not hasBodyParsed:
                        headers = self.ParseBody(kwargs.get('body'),client,headers) # Await for additional messages
                    else:
                        headers[0]['IP'] = self.get_client_ip(client)
                    msg : str = URLS.get(url).__call__(headers) #Call the view
                    assert type(msg) in (tuple,bytes),"Response must only return ({},{}) by calling __call__ on the response, you return {}.".format(bytes,tuple,type(msg))
                    if isinstance(msg,tuple): #Binary file
                        with open(msg[1],'rb+') as file:
                            initial = self.HandleCORS(msg[0](getsize(msg[1])),headers) #Send the HTTP Headers with the file lenght
                            client.send(initial)
                            try:
                                for chunk in lazy_read(file):
                                    client.send(chunk) #Lazy-send the chunks
                            except:
                                return client.close() # Any error due to exit
                    else:
                        client.send(self.HandleCORS(msg,headers))
                except Exception as f:
                    print_exception(type(f),f,f.__traceback__)
                    client.send(status.Http500().__call__(self.page500))
                finally:
                    return client.close()
        #Page was not found
        client.send(status.Http404().__call__(self.page404(target)))
        return client.close()

    def AwaitRequest(self):
        """Wait for requests to be made"""
        self.connection.listen(1)
        #Start thread not to block request
        while True:
            client = self.connection.accept()
            t = threading.Thread(target=self.HandleRequest,args=(client,self.urls))
            t.start()

    def HandleRequest(self,client,URLS : dict):
        """
           ** Method that handles the requests\r
           ** when they are first made,\r
           ** giving the the target route view\r
           ** and then closing the connection\r
           ** Called Only once and then thread exits\r
        """
        client,address = client 
        client.settimeout(5)
        try:
            request = client.recv(self.receive_size) #Await for messages
        except:
            return client.close()     

        if len(request) == 0:
            return client.close()

        headers = ParseHTTP(request,lambda : client.recv(self.receive_size))

        print(f'(HTTP) : {headers[0]["method"]} | {str(datetime.now())} : {address}')
        return self.handleHTTP(client,headers, URLS)

    def get_client_ip(self,client):
        return client.getsockname()[0]

    def handleTraceback(self,function,fname,path : str =  None):
        try:
            res = function(0)
            return res
        except Exception as f:
            path = path if path is not None else ''
            print(f"[ERROR] (WS) {path} : {str(datetime.now())} An Exception occurred while calling the {fname} function")
            print_exception(type(f),f,f.__traceback__)
            return False

    def start(self):
        print(f'({str(datetime.now())}) HTTP Server has gone live.')
        return self.AwaitRequest()

class WebsocketServer(HttpServer):
    """An extension of the HTTP Server for handling WebSocket Protocols\n
       Only one WebSocket server 'route' can be maintained at the same time\n
       on the exact same ADDRESS and PORT using this class.

       param: host : str = LOCALHOST (127.0.0.1)  
       param: port : int = 8000
       param max_size : int = 4096 (The Maximun number of data that can be transmitted in one Message)
    """

    def __init__(self,host : str = LOCALHOST,port : int = 8000,max_size : int = 1024,**kwargs):
        self.clients : list = [] #Store all the clients
        self.max_size = max_size
        isHttp = kwargs.get('http')
        super(WebsocketServer,self).__init__(host=host,port=port,http=f'{"WS" if isHttp is None else "Standar Server"}',**kwargs)
        del isHttp
        if (not kwargs.get('rdel')):
            del self.urls,self.page404,self.page500

    def AwaitSocket(self,add_to_clients : bool = True):
        """Wait for new connections"""
        self.connection.listen(1)
        while True:
            client,adress = self.connection.accept()
            threading.Thread(target=self.handleWebSocket,args=(client,adress)).start()

    def onMessage(self,**kwargs):
        """Gets called when a message is received from the client side"""
        pass

    def onExit(self,client,**kwargs):
        """Called when a client exits
          the 'client' paramter is part
          of the socket library 
        """
        pass
    
    def onConnect(self,client,**kwargs):
        """Called when a client establishes
          a connection to the server,
          the 'client' paramter is part
          of the socket library 
        """
        pass

    def send(self,client : socket.socket,data : str) -> None:
        """Sends data to a client"""
        client.send(SocketBinSend(data))

    def handleDisconnect(self,client : socket.socket ,list_of_clients : Any = None):
        if list_of_clients is None:
            CLS = self.clients
            indx = CLS.index(client)
            self.clients.pop(indx)
            client.close()
            return self.handleTraceback(lambda _ : self.onExit(client,send_function=self.send),'onExit')
        else:
            CLS = list_of_clients
            CLS.pop(client) 
            # indx = CLS.index(client)
            # CLS.pop(indx)
            client.close()
            return self.handleTraceback(lambda _ : self.onExit(client,send_function=self.send),'onExit')

    def accept(self,client : socket.socket,**kwargs) -> None:
        key = kwargs.get('key')
        return client.send(status.Http101().__call__(key))

    def handleWebSocket(self,client,address,**kwargs):
        #TODO 2 client.settimeout(5) # Wait 5 seconds for connection to be established
        client.settimeout(4)
        
        try:
            data = client.recv(1024)
        except:
            return client.close()

        client.settimeout(None)
        data = data.split(b'\r\n\r\n',1)
        headers = ParseHeaders(data[0]) #request body is reduntant


        EnsureSocket(headers,(client,address))
        hndl = self.handleTraceback(lambda x : self.onConnect(client,adress=address,send_function=self.send,key=headers['Sec-WebSocket-Key']),"onConnect")                

        if not hndl:
            print(f"(WS) : {str(datetime.now())} Connection Closed because bool(onConnect) return False {address}")
            return client.close() #Close if there was an Exception or return None

        #Increment the number of clients and print 
        num_client : int = self.clients.__len__()+1
        print(f"(WS) : {str(datetime.now())} Connection Established ({num_client} Client{'s' if num_client > 1 else ''}) {address}")

        #Add them to the clients-list (current route)
        self.clients.append(client)

        while True:
            try:
                data = client.recv(self.max_size)
            except:
                print(f"(WS) : {str(datetime.now())} Connection Closed {address}")
                return self.handleDisconnect(client)

            if len(data) == 0 or data[0] == 136: # if 0th byte == 136 is exit code
                print(f"(WS) : {str(datetime.now())} Connection Closed {address}")
                return self.handleDisconnect(client)

            fin = data[1] & 127 # for decoding the length of the message

            if fin in (126,127):
                decoded = DataWait(fin,data,lambda : client.recv(self.max_size),self.max_size,prnt_func=lambda pld: print(f"(WS) : {str(datetime.now())} Received Message (Payload : {pld}) {address}"))
                self.handleTraceback(lambda x : self.onMessage(data=decoded,sender_client=client),"onMessage")                                
                continue

            print(f"(WS) : {str(datetime.now())} Received Message (Payload {fin}) {address}")
            decoded = SocketBin(data)
            self.handleTraceback(lambda x : self.onMessage(data=decoded,sender_client=client),"onMessage")                                

    def start(self):
        print(f'({str(datetime.now())}) WS Server has gone live.')
        return self.AwaitSocket()

class RoutedWebsocketServer(WebsocketServer):
    """
    A Websocket Server that can have multiple routes,
    each one having it's own seperate clients,
    all running on the same ADDRESS and PORT

    Additional Parameters to WebsocketServer:
        param: global_max_size : int = 4096 (This is the message that is transmitted before establishing a connection during the WebSocket HANDSHAKE)

    """

    def __init__(self,paths : dict,host : str = LOCALHOST,port : int = 8000,global_max_size : int = 4096,**kwargs):
        self.global_max_size = global_max_size
        self.routes : dict = {}
        err_msg = f'Dictionary Value specifying view must inherit from {SocketView}.'
        for item in paths:
            assert type(item) == str, "Dictionary Key specifying path must be {} not {}".format(str,type(item))
            assert issubclass(type(paths[item]),SocketView),err_msg 
            self.routes[item] =  {"clients" : {},"view" : paths[item]}
        super(RoutedWebsocketServer,self).__init__(host,port,**kwargs)
        del self.clients,self.max_size

    def AwaitSocket(self):
        super(RoutedWebsocketServer,self).AwaitSocket()

    def handleWebSocket(self,client,address,**kwargs):
        headers = kwargs.get('headers')

        if not kwargs.get('dont_wait'):
            client.settimeout(5)
            try:
                data = client.recv(self.global_max_size)
            except:
                return client.close()
            client.settimeout(None)
            headers : dict = ParseHeaders(data.split(b'\r\n\r\n')[0]) # Request body is redundant
        else:
            headers = kwargs.get('headers')

        EnsureSocket(headers,(client,address))

        #Check if the path is found
        path : str = headers['method'].split(" ",1)[1]
        if not path in self.routes:
            print(f"(WS) : {str(datetime.now())} Connection Not Found \"{path}\" {address}")
            return client.close()

        #Get The View and call the onConnect function
        CWM = self.routes[path]["view"]
        hndl = self.handleTraceback(lambda _ : CWM.onConnect(client=client,path_info=self.routes[path],send_function=self.send,headers=headers,key=headers['Sec-WebSocket-Key']),"onConnect",path)  
        
        if not hndl:
            print(f"(WS) {path} : {str(datetime.now())} Connection Closed because bool(onConnect) return False {address}")
            return client.close() #Close if there was an Exception or return None
        
        #Increment the number of clients and print 
        num_client : int = self.routes[path]['clients'].__len__()+1
        print(f"(WS) {path} : {str(datetime.now())} Connection Established ({num_client} Client{'s' if num_client > 1 else ''}) {address}")

        #Add them to the clients-list (current route)
        # self.routes[path]['clients'].append(client)
        self.routes[path]['clients'][client] = hndl # hndl returns state

        while True:
            try:
                data = client.recv(CWM.MaxSize())
            except:
                self.handleDisconnect(client,self.routes[path]['clients'])
                self.handleTraceback(lambda _ : CWM.onExit(client,path_info=self.routes[path],send_function=self.send),'onExit')
                break

            if len(data) == 0 or  data[0] == 136: #136 exit code
                print(f"(WS) {path} : {str(datetime.now())} Connection Closed {address}")
                self.handleDisconnect(client,self.routes[path]['clients'])
                self.handleTraceback(lambda _ : CWM.onExit(client,path_info=self.routes[path],send_function=self.send),'onExit')
                break

            fin = data[1] & 127 #Decode the length of the message
            if fin in (126,127):
                decoded = DataWait(fin,data,lambda : client.recv(CWM.MaxSize()),CWM.MaxSize(),prnt_func=lambda pld: print(f"(WS) {path} : {str(datetime.now())} Received Message (Payload : {pld}) {address}"))
                self.handleTraceback(lambda x : CWM.onMessage(data=decoded,sender_client=client,path_info=self.routes[path],send_function=self.send),"onMessage")                                
                continue
            
            print(f"(WS) {path} : {str(datetime.now())} Received Message {address}")
            decoded = SocketBin(data)    
            self.handleTraceback(lambda _ : CWM.onMessage(data=decoded,sender_client=client,path_info=self.routes[path],send_function=self.send),"onMessage",path)

class Server(RoutedWebsocketServer):
    """
        Server that can handle both websocket and HTTP connections\n
        concurrently at the same adress and port. The way connections\n
        are distinguished is by looking at the Upgrade header's value.\n
        if it is not present or it is anything else other than 'websocket'\n
        then it is interpeted as HTTP else it is authenticated as ws.\n 
    """
    
    def __init__(self,socket_paths : dict, http_paths : dict ,host : str = LOCALHOST,port : int = 8000,global_max_size : int = 1024,CORS_DOMAINS : list = [],**kwargs) -> None:
        super(Server, self).__init__(socket_paths,host,port,global_max_size,URLS=http_paths,rdel=1,CORS_DOMAINS=CORS_DOMAINS)
    
    def HandleRequest(self,client : socket.socket , URLS : dict) -> None:
        client,address = client 
        client.settimeout(5) # 5 sec wait time
        try:
            request : bytes = client.recv(1024)
        except:
            return client.close()
            
        client.settimeout(None) # clear the timeout

        if len(request) == 0:
            return client.close()
        
        spl = request.split(b'\r\n\r\n',1)
        try:
            headers,body = spl
            headers = ParseHeaders(headers)
        except:
            print(f"[ERROR] : {str(datetime.now())} | Invalid Request From client ({address})")
            return client.close()

        #WebSocket Connection
        if 'Upgrade' in headers:
            if headers['Upgrade'].lower()=='websocket':
                print(f'(WS) : {headers["method"]} | {str(datetime.now())} : {address}')
                return threading.Thread(target=self.handleWebSocket,args=(client,address), kwargs={'headers' : headers,'dont_wait' : True}).start()
        
        #Normal HTTP Connection
        print(f'(HTTP) : {unquote(headers["method"])} | {str(datetime.now())} : {address}')
        return threading.Thread(target=self.handleHTTP,args=(client,headers,URLS),kwargs={'body' : body}).start()

    def start(self):
        print(f'({str(datetime.now())}) HTTP && WS Server has gone live.')
        return self.AwaitRequest()


if __name__ == '__main__':
    pass