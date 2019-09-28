from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
from test_python.test_python.utils import rs
import redis
import pickle
# rs = redis.StrictRedis(host='localhost', port=6379, db=1)
wss=[]
class SimpleEcho(WebSocket):

    # def handleMessage(self):
    #     # echo message back to client
    #     # self.sendMessage(self.data)
    #     if self.data is None:
    #         self.data = 'test'
    #
    #     for ws in wss:
    #         ws.sendMessage(str(self.data))

    def handleConnected(self):
        # self.test()
        print(self.address, 'connected')
        if self not in wss:
            wss.append(self)
        # for ws in wss:
        #     ws.sendMessage(str(self.address))
        print(wss.__len__())


    def handleClose(self):
        wss.remove(self)
        print(self.address, 'closed')

def alert():
    if rs.get('update'):
        rs_data = rs.get('update').decode('utf-8')
        if wss:
            for ws in wss:
                ws.sendMessage(str(rs_data))
    # t=threading.Timer(550.0,alert)
    t = threading.Timer(550.0, alert)
    t.start()

server = SimpleWebSocketServer('', 8001, SimpleEcho)
alert()
server.serveforever()
