from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import threading
import redis
import pickle
rs = redis.StrictRedis(host='localhost', port=6379, db=1)
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

def test():
    if rs.get('update'):
        rs_data = rs.get('update').decode('utf-8')
        if wss:
            for ws in wss:
                ws.sendMessage(str(rs_data))
    t=threading.Timer(5.0,test)
    t.start()

server = SimpleWebSocketServer('', 8001, SimpleEcho)
test()
server.serveforever()

#
# import asyncio
# import datetime
# import random
# import websockets
# import transaction
# from pyramid.threadlocal import get_current_registry
# from test_python.test_python.models import (
#             get_engine,
#             get_session_factory,
#             get_tm_session,
#             )
#
# from test_python.test_python import models
# from test_python.test_python.utils import get_answers_to_api
# from sqlalchemy import func
#
# async def time(websocket, path):
#     while True:
#         registry = get_current_registry()
#         settings = registry.settings
#         engine = get_engine(settings)
#         session_factory = get_session_factory(engine)
#         with transaction.manager:
#             dbsession = get_tm_session(session_factory, transaction.manager)
#             list_requests = dbsession.query(models._Request).all()
#             print(list_requests)
#
#         # now = datetime.datetime.utcnow().isoformat() + "Z"
#         await websocket.send('test')
#         await asyncio.sleep(random.random() * 3)
#
# start_server = websockets.serve(time, "127.0.0.1", 5678)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
#
