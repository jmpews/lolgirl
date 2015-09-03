__author__ = 'jmpews'
import threading
from logger import initLogging

# log file
loggg=initLogging('threadpool.log')

# 初始化工作函数和线程数
class ThreadPool(object):
    def __init__(self,func=None,thread_num=5):
        self.threads=[]
        if func==None:
            self.func=None
            print('Error : func is None...')
            return
        self.func=func
        self.__init_threads(thread_num)

    def __init_threads(self,thread_num=5):
        for i in range(thread_num):
            self.threads.append(Worker(self.func))

    def start(self):
        if self.func==None:
            print('func is None...')
            return
        for one in self.threads:
            one.start()

# 线程实例
class Worker(threading.Thread):
    def __init__(self,func=None):
        self.func=func
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                self.func()
            except Exception as e:
                loggg.error(e)
                import traceback
                traceback.print_exc()
            print('======='+self.name+'Done!=======')

# 测试函数
def test():
    def func():
        print('oh,yes!')
    threadpool=ThreadPool(func=func)
    threadpool.start()

#test()