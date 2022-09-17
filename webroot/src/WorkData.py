import threading
from socket import SHUT_RDWR

class WorkData(threading.Thread):
    ConnectingThread = []
    
    def __init__(self, newsocket, client_addr, mylog):
        super(WorkData, self).__init__()
        self.newsocket = newsocket
        self.client_addr = client_addr
        self.mylog = mylog
    # TODO 何时断开连接
    def run(self):
        try:
            rec = self.newsocket.recv(1024).decode("utf-8")
            print(rec)
            response = "HTTP/1.1 404 NOT FOUND\r\n "
            response += "\r\n"
            response += "file not found!!!!"
            self.newsocket.send(response.encode("utf-8"))
        except IOError:
            self.mylog.LogError("send error")
        finally:
            WorkData.ConnectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
