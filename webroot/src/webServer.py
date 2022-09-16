import socket
import parameter
import log

def  WebServer():
    #tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #udp socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    # setsockopt
    # 绑定
    server.bind((parameter.ip, parameter.port))
