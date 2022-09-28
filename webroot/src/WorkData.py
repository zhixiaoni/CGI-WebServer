import os
import threading
import parameter
import re
from socket import SHUT_RDWR

class Response():
    #详见http格式.txt
    #状态行
    #400 客户端请求有语法错误; 403 收到请求但拒绝服务; 404 请求资源不存在
    statusLineDict = {200 : "HTTP/1.0 200 OK\r\n",\
        400 : "HTTP/1.0 400 Bad Request\r\n",\
        403: "HTTP/1.0 403 Forbidden\r\n",\
        404: "HTTP/1.0 404 Not Found\r\n"}
    #类型
    contentTypeDict = {"text":"Content-Type: text/html; charset=UTF-8\r\n",\
        "image":"Content-Type: image/jpg\r\n"}
    
    # contentLength = "Content-Length: "
    #空行
    blankLine = "\r\n"
    
    def __init__(self, mylog):
        #默认预置200
        self.statusLine = "HTTP/1.0 200 OK\r\n"
        #默认预置为text
        self.contentType = "text"
        
        self.header = ""
        # self.header = Response.contentLength \
        #     + Response.contentTypeDict[self.contentType] \
        #     +"Connection: close\r\n"            
        self.blankLine = Response.blankLine
        self.body = ""
        
        #日志类
        self.mylog = mylog
    
    #设置状态行
    def SetStatusLine(self, status = 200):
        self.statusLine = Response.statusLineDict[status]
    
    #设置Header        
    def SetHeader(self):
        self.header = Response.contentTypeDict[self.contentType] \
            +"Connection: close\r\n"
            
        # self.header = Response.contentLength \
        #     + str(len(self.body)) \
        #     + "\r\n" \
        #     + Response.contentTypeDict[self.contentType] \
        #     +"Connection: close\r\n"
    
    def SetContentType(self, contentType = "text"):
        self.contentType = contentType
    
    def SetBody(self, body = ""):
        self.body = body
    
    
    #设置Body  
    #Get方法，考察访问权限，直接返回路径下的文件
    def SetGetBody(self, path = parameter.index_path):
        if not (path == parameter.index_path or path == parameter.html404_path or \
            path.startswith(parameter.html_path) or path.startswith(parameter.CGI_path) or \
                path.startswith(parameter.picture_path)):
            raise IOError
        if self.contentType == "image":
            f = open(path, mode = "rb")
            self.body = f.read()
            f.close()
        else:
            f = open(path, mode = "r", encoding = 'utf-8')
            self.body = f.read()
            f.close()
        
    # TODO 
    # Post方法，调用CGI
    def SetPostBody(self):
        pass
        
    #输出最终报文结果
    def GetRes(self):
        if self.contentType == "image":
            return (self.statusLine + self.header + self.blankLine).encode("utf-8"), self.body
        else:
            return (self.statusLine + self.header + self.blankLine).encode("utf-8"), self.body.encode("utf-8")


class WorkData(threading.Thread):
    connectingThread = []
    
    def __init__(self, newsocket, client_addr, mylog):
        super(WorkData, self).__init__()
        self.newsocket = newsocket
        self.client_addr = client_addr
        self.mylog = mylog
    
    def SendResponse(self, response):
        self.newsocket.send(response.GetRes()[0])
        self.newsocket.send(response.GetRes()[1])
        
        
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
    
    def Resolv2(self, recvData):
        pattern = re.compile("(.*?)(\r\n.*?)(User-Agent: )(.*?)(\r\n.*)",re.S)
        m = pattern.match(recvData)
        request = m.group(1)
        userAgent = m.group(4)
        return request, userAgent

     
    def Deal400(self, response, request, userAgent):
        response.SetStatusLine(400)
        response.SetHeader()
        response.SetGetBody(path = parameter.html400_path)
        self.SendResponse(response)
        self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 400,\
                len(response.GetRes()[-1]), userAgent)) 
         
 
    
    def Deal404(self, response, request, userAgent):
        response.SetHeader()
        self.mylog.LogError("path not correct")
        response.SetGetBody(path = parameter.html404_path)
        response.SetStatusLine(404) 
        self.SendResponse(response)
        self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 404,\
            len(response.GetRes()[-1]), userAgent))        

       
    def DealGet(self, response, path, request, userAgent):
        if path.endswith(("jpeg","jpg")):
            response.SetContentType("image") 
        else:
            response.SetContentType("text") 
        try:
            response.SetGetBody(path = path)
            response.SetStatusLine(200) 
            response.SetHeader()
            self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 200,\
                len(response.GetRes()[-1]), userAgent))
        except:
            response.SetContentType("text")
            self.mylog.LogError("forbidden")
            response.SetGetBody(path = parameter.html403_path)
            response.SetStatusLine(403) 
            response.SetHeader()
            self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 403,\
                len(response.GetRes()[-1]), userAgent))
        finally:
            self.SendResponse(response)              
    
    #和Get方法一样，不过最后把body设为"" 
    def DealHead(self, response, path, request, userAgent):
        if path.endswith(("jpeg","jpg")):
            response.SetContentType("image") 
        else:
            response.SetContentType("text") 
        try:
            response.SetGetBody(path = path)
            response.SetBody("")
            response.SetStatusLine(200) 
            response.SetHeader()
            self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 200,\
                len(response.GetRes()[-1]), userAgent))
        except:
            response.SetContentType("text")
            self.mylog.LogError("forbidden")
            response.SetGetBody(path = parameter.html403_path)
            response.SetBody("")
            response.SetStatusLine(403) 
            response.SetHeader()
            self.mylog.LogInfo(self.mylog.StdInfo(self.client_addr, request, 403,\
                len(response.GetRes()[-1]), userAgent))
        finally:
            self.SendResponse(response)      
        
    # 解析和发送
    def run(self):
        try:
            recvData = self.newsocket.recv(1024).decode("utf-8")
            print(recvData)
            
            method, path, resolvRes = self.Resolv(recvData)
            
            response = Response(self.mylog)
            # 解析失败 有语法错误 返回400
            if not resolvRes:
                self.Deal400(response = response, request = "", userAgent = "")
                raise IOError
            
            request, userAgent = self.Resolv2(recvData)
            
            #文件不存在 404
            if not os.path.exists(path = path):
                self.Deal404(response = response, request = request, userAgent =userAgent)  
                raise IOError

            #GET方法
            if method == "GET":
                self.DealGet(response = response, path = path, request = request, userAgent =userAgent)
            #POST方法
            elif method == "POST":
                pass    
            #HEAD方法
            else:
                self.DealHead(response = response, path = path, request = request, userAgent =userAgent) 
            #print(response.GetRes())
        except IOError:
            self.mylog.LogError("send error")
        finally:
            WorkData.connectingThread.remove(self)
            self.newsocket.shutdown(SHUT_RDWR)
            self.newsocket.close()
