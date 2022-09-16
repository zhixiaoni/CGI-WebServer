import socket
import parameter
import WorkData
from log import LogInfo

def  WebServer():
    #tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #udp socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    # 日志就照着这个写
    LogInfo("start tcp socket")
    
    # setsockopt
    
    # 绑定
    server.bind((parameter.ip, parameter.port))
    
    # 缓冲队列中的最大数目
    server.listen(parameter.MaxWaiting)
    
    while True:
        
        # 线程控制 最大数目 parameter.MaxConnection
        
        # 接受
        newsocket, client_addr = server.accept()
        
        # 创建新线程处理连接
        
