import socket
import parameter
from WorkData import WorkData
from log import MyLog

def  WebServer():
    mylog = MyLog()
    #tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #udp socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    # 日志就照着这个写
    mylog.LogInfo("start tcp socket")
    
    # setsockopt 超时断连等设置
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定
    server.bind((parameter.ip, int(parameter.port)))
    
    # 缓冲队列中的最大数目
    server.listen(parameter.MaxWaiting)
    
    while True:
        
        # 线程控制 最大数目 parameter.MaxConnection
        if len(WorkData.ConnectingThread) < parameter.MaxConnection:
            # 接受
            newsocket, client_addr = server.accept()
            # 创建新线程处理连接
            WorkData.ConnectingThread.append(WorkData(newsocket, client_addr, mylog))    #加入队列
            WorkData.ConnectingThread[-1].setDaemon(True)   #设为守护进程
            WorkData.ConnectingThread[-1].start()   #开始
        
