Very **simple** way to interact with any http and Websocket requests

```python
from darius.server import server,routes
from darius.client_side import status

class Home(routes.View):
    def GET(self,request,**kwargs):
        return status.Http200().__call__("<h1>Home Page</h1>")
    
    def POST(self,request,**kwargs):
        return status.HttpBinary().__call__("dog.png",display_in_browser=True)

    def __init__(self,*args,**kwargs): 
        """Optional : Add your own custom HTTP method requests"""
        super(Home,self).__init__(*args,**kwargs)
        self.cases['CREATE'] = self.POST # Custom HTTP method

class Chat(routes.SocketView):
    def onConnect(self,client,**kwargs):
        key = kwargs.get("key")
        username = kwargs.get("headers")['Cookies']['username']
        self.accept(client,key)
        return {"username" : username,"id" : ord(username[0]) % 51} # Stored as state with client
    
    def onMessage(self,client,**kwargs):
        data = kwargs.get('data') # Message sent
        path_info = kwargs.get("path_info") # Containing information about clients
        send = kwargs.get('send_function') # Functions to send data

        # Send the message to every client
        for client in path_info['clients']:
            if(client['username'].startswith("a")) or client['id'] % 2 == 0:
                send(client,data)
    
    def onExit(self,client,**kwargs):
        print("Client exited!")
```
And then to actually list the paths and start the Server

```python
WS_URLS = {
    r'/chat(\/)?' : Chat()
}

HTTP_URLS = {
    r'/home(\/)?' : Home()
}

server.Server(WS_URLS,HTTP_URLS,port=8000).start()
```

More can be found at [Github](https://github.com/Greece4ever/darius)