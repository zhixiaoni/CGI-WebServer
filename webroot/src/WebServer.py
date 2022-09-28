import socket
import parameter
import threading
from WorkData import WorkData
from ThreadPool import ThreadPool
from log import MyLog

def  WebServer():
    mylog = MyLog()
    #tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #udp socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


    mylog.LogInfo("start tcp socket")
    
    # setsockopt 超时断连等设置
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定
    server.bind((parameter.ip, parameter.port))
    
    # 缓冲队列中的最大数目
    server.listen(parameter.maxWaiting)
    
    pool = ThreadPool(parameter.maxConnection)
    
    while True:
        
        # 线程控制 最大数目 parameter.MaxConnection
        if len(WorkData.connectingThread) < parameter.maxConnection:
            # 接受
            newsocket, client_addr = server.accept()
            # 创建新线程处理连接
            # print("Thread main id: "+str(threading.current_thread), threading.active_count())
            pool.submit(WorkData,(newsocket, client_addr, mylog,))
            # WorkData.connectingThread.append(WorkData(newsocket, client_addr, mylog))    #加入队列
            # WorkData.connectingThread[-1].setDaemon(True)   #设为守护进程
            # WorkData.connectingThread[-1].start()   #开始
        
