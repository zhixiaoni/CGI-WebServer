import threading
from socket import SHUT_RDWR
from log import LogInfo
from log import LogError
class WorkData(threading.Thread):
    ConnectingThread = []
    
    def __init__(self, newsocket, client_addr):
        super(WorkData, self).__init__()
        self.newsocket = newsocket
        self.client_addr = client_addr
        
        
    def run(self):
        try:
            self.newsocket.recv(1024).decode("utf-8")
            response = "HTTP/1.1 404 NOT FOUND\r\n "
            response += "\r\n"
            response += "file not found!!!!"
            self.newsocket.send(response.encode("utf-8"))
        except IOError:
            LogError("send error")
        finally:
            WorkData.ConnectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
