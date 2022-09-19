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
        pattern = re.compile("([a-zA-Z]+)([ /]*)([a-zA-Z0-9./]*)( HTTP/1.1)(.*)", re.S)
        m = pattern.match(recvData)
        try:
            method = m.group(1)
            if m.group(3) == "":
                path = parameter.index_path
            else:
                path = os.path.join(parameter.webroot_path, m.group(3))
            return method, path, True
        except:
            self.mylog.LogError("resolv error")
            return "", "", False
        
    def Deal400(self, response):
        response.SetStatusLine(400)
        response.SetHeader("text")
        response.SetGetBody(path = parameter.html400_path)
        self.newsocket.send(response.GetRes())
    
    def DealGet(self, response, path):
        try:
            response.SetGetBody(path = path)
            response.SetStatusLine(200) 
        except:
            self.mylog.LogError("path not correct")
            response.SetGetBody(path = parameter.html404_path)
            response.SetStatusLine(404) 
        finally:
            response.SetHeader("text") 
            self.newsocket.send(response.GetRes())              
        

    # TODO 解析和发送
    def run(self):
        try:
            recvData = self.newsocket.recv(1024).decode("utf-8")
            print(recvData)
            
            method, path, resolvRes = self.Resolv(recvData)
            
            #TODO:根据解析 发送对应的报文
            response = Response(self.mylog)
            # 解析失败 有语法错误 返回400
            if not resolvRes:
                self.Deal400(response = response)
                raise IOError
            
            #GET方法
            if method == "GET":
                self.DealGet(response = response, path = path)
            #POST方法
            elif method == "POST":
                pass    
            else:
                pass  
            #print(response.GetRes())
        except IOError:
            self.mylog.LogError("send error")
        finally:
            WorkData.connectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
