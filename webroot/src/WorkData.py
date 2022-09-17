import threading
from socket import SHUT_RDWR

class WorkData(threading.Thread):
    ConnectingThread = []
    
    def __init__(self, newsocket, client_addr, mylog):
        super(WorkData, self).__init__()
        self.newsocket = newsocket
        self.client_addr = client_addr
        self.mylog = mylog
        
    # TODO 解析和发送
    def run(self):
        try:
            RecvData = self.newsocket.recv(1024).decode("utf-8")
            print(RecvData)
            
            # 解析RecvData
            
            
            
            #根据解析 发送对应的报文
            
            response = "HTTP/1.1 200 OK\r\n "
            response += "Content-Length: 128\r\n"
            response += "Content-Type: text/html; charset=UTF-8\r\n"
            response += "Connection: close\r\n"
            response += "\r\n"
            response += """<html>
<body>
finnaly success
</body>
</html>"""

            self.newsocket.send(response.encode("utf-8"))
            print(response)
        except IOError:
            self.mylog.LogError("send error")
        finally:
            WorkData.ConnectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
