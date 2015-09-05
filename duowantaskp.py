__author__ = 'jmpews'

import time

import requests
import utils
from redisq import RedisQueue
from logger import initLogging

import re

from bs4 import BeautifulSoup

# 每类url由一个线程处理,总共有三个线程处理
# 提交到redis使用with做好线程锁处理,最后想了下发现并不需要锁.

t_start=int(time.time())
rq=RedisQueue('dwgirl')
import threading


def qqlol():
    pre_url=r"http://bbs.lol.qq.com/"
    url="http://bbs.lol.qq.com/forum.php?mod=forumdisplay&fid=205&typeid=966&typeid=966&filter=typeid&page=%d"
    i=0
    while True:
        time.sleep(1)
        # 计数循环
        i+=1
        i=i%1000
        i=1 if i==0 else i
        purl=url % i
        r=requests.get(purl)
        p=re.compile('我要曝照</a>\]</em> <a href="(.+?)"')
        # urls=[pre_url+x for x in p.findall(r.text)]
        urls=p.findall(r.text)
        if urls is None:
            continue
        for x in urls:
            tmp=pre_url+utils.quote_url(x)
            rq.put(tmp)
            print(tmp)
        print('=========qqlol-',i,' =========')

def duowanlol1():
    pre_url=r"http://bbs.duowan.com/"
    url="http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1343&orderby=dateline&typeid=7092&filter=author&orderby=dateline&typeid=7092&page=%s"
    i=0
    while True:
        time.sleep(1)
        # 计数循环
        i+=1
        i=i%1000
        i=1 if i==0 else i
        purl=url % i
        r=requests.get(purl)
        p=re.compile('求封面</a>\]</em> <span id="thread_\d+?"><a href="(.+?)"')
        # urls=[pre_url+x for x in p.findall(r.text)]
        urls=p.findall(r.text)
        if urls is None:
            continue
        for x in urls:
            tmp=pre_url+utils.quote_url(x)
            rq.put(tmp)
            print(tmp)
        print('=========duowan1-',i,' =========')

def duowanlol2():
    pre_url=r"http://bbs.duowan.com/"
    url="http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1343&orderby=dateline&typeid=3317&orderby=dateline&typeid=3317&filter=author&page=%s"
    i=0
    while True:
        time.sleep(1)
        # 计数循环
        i+=1
        i=i%1000
        i=1 if i==0 else i
        purl=url % i
        r=requests.get(purl)
        p=re.compile('自曝</a>\]</em> <span id="thread_\d+?"><a href="(.+?)"')
        # urls=[pre_url+x for x in p.findall(r.text)]
        urls=p.findall(r.text)
        print(urls)
        if urls is None:
            continue
        for x in urls:
            tmp=pre_url+utils.quote_url(x)
            with lock:
                rq.put(tmp)
            print(tmp)
        print('=========duowan2-',i,' =========')

lock=threading.Lock()
a=threading.Thread(target=qqlol)
b=threading.Thread(target=duowanlol1)
c=threading.Thread(target=duowanlol2)
a.start()
# b.start()
# c.start()