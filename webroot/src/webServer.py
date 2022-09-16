import socket
import parameter
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
