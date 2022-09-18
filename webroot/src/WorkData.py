import os
import threading
import parameter
import re
from socket import SHUT_RDWR

class Response():
    #详见http格式.txt
    #状态行
    #400 客户端请求有语法错误; 403 收到请求但拒绝服务; 404 请求资源不存在
    statusLineDict = {200 : "HTTP/1.1 200 OK\r\n",\
        400 : "HTTP/1.1 400 Bad Request\r\n",\
        403: "HTTP/1.1 403 Forbidden\r\n",\
        404: "HTTP/1.1 404 Not Found\r\n"}
    #类型
    contentTypeDict = {"text":"Content-Type: text/html; charset=UTF-8\r\n",\
        "image":"Content-Type: image/jpg\r\n"}
    
    contentLength = "Content-Length: 65536\r\n"
    #空行
    blankLine = "\r\n"
    
    def __init__(self, mylog):
        #默认预置200
        self.statusLine = "HTTP/1.1 200 OK\r\n"
        #默认预置为text
        self.header = Response.contentLength \
            + Response.contentTypeDict["text"] \
            +"Connection: close\r\n"
            
        self.blankLine = Response.blankLine
        self.body = ""
        
        #日志类
        self.mylog = mylog
    
    #设置状态行
    def SetStatusLine(self, status = 200):
        self.statusLine = Response.statusLineDict[status]
    
    #设置Header        
    def SetHeader(self, contentType = "text"):
        self.header = Response.contentLength \
            + Response.contentTypeDict[contentType] \
            +"Connection: close\r\n"
    
    #设置Body  
    #Get方法，直接返回路径下的文件
    def SetGetBody(self, path = parameter.index_path):
        f = open(path, mode = "r", encoding = 'utf-8')
        self.body = f.read()
        f.close()
        
    # TODO 
    # Post方法，调用CGI
    def SetPostBody(self):
        pass
        
    #输出最终报文结果
    def GetRes(self):
        return (self.statusLine + self.header + self.blankLine + self.body).encode("utf-8")


class WorkData(threading.Thread):
    connectingThread = []
    
    def __init__(self, newsocket, client_addr, mylog):
        super(WorkData, self).__init__()
        self.newsocket = newsocket
        self.client_addr = client_addr
        self.mylog = mylog
    
    def Resolv(self, recvData):
        pattern = re.compile("([a-zA-Z]+)([ /]*)([a-zA-Z0-9.]*)( HTTP/1.1)(.*)", re.S)
        m = pattern.match(recvData)
        method = m.group(1)
        if m.group(3) == "":
            path = parameter.index_path
        else:
            path = os.path.join(parameter.webroot_path, m.group(3))
        return method, path
    
    # TODO 解析和发送
    def run(self):
        try:
            recvData = self.newsocket.recv(1024).decode("utf-8")
            print(recvData)
            
            # TODO:解析RecvData
            method, path = self.Resolv(recvData)
            
            #TODO:根据解析 发送对应的报文
            response = Response(self.mylog)
            response.SetStatusLine(200) #默认200，可以不设置
            response.SetHeader("text") #默认为text，可以不设置
            response.SetGetBody(path = path)
            self.newsocket.send(response.GetRes())
            #print(response.GetRes())
        except IOError:
            self.mylog.LogError("send error")
        finally:
            WorkData.connectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
