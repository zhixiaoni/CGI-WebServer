import queue
from re import S, T
import threading
from WorkData import WorkData

StopEvent = object()

class ThreadPool(object):
    def __init__(self, maxConnection):
        self.taskQueue = queue.Queue(maxConnection)
        self.maxConnection = maxConnection
        self.cancel = False
        self.terminal = False
        self.activeThread = []
        self.freeThread = []

    def submit(self, task, args):
        # if self.cancel:
        #     return

        if not self.freeThread and \
            len(self.activeThread) < self.maxConnection:
            threading.Thread(target = self.getTask).start()
        self.taskQueue.put((task,args))

    def getTask(self):
        self.freeThread.append(threading.currentThread())

        task, args = self.taskQueue.get()

        while task != StopEvent:
            # print("task:", task)
            # print("args:", args)
            # print("Thread num: ", len(self.activeThread), len(self.freeThread))
            # print("Thread get id: "+str(threading.current_thread))
            self.activeThread.append(threading.currentThread())
            self.freeThread.remove(threading.currentThread())

            task(*args).run()
            
            self.freeThread.append(threading.currentThread())
            self.activeThread.remove(threading.currentThread())

            if self.terminal:
                task = StopEvent
            else:
                task, args = self.taskQueue.get()

    def close(self):
        self.cancel = True
        while self.activeThread:
            self.taskQueue.put(StopEvent)
        self.taskQueue.queue.clear()

