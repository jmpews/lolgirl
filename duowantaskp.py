__author__ = 'jmpews'

import time

import requests
import utils
from redisq import RedisQueue
from logger import initLogging

import re

from bs4 import BeautifulSoup

pre_url=r"http://bbs.duowan.com/"
purl="http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1343&orderby=dateline&typeid=3317&orderby=dateline&typeid=3317&filter=author&page=%s"


t_start=int(time.time())
rq=RedisQueue('dwgirl')

i=1000
lasttime=0
lasturl=[]
while True:
    print('one loop...')
    i=i-1 if i>1 else 1
    requesturl=purl % (i)
    print('=====Page.',i,'=====')
    r=requests.get(requesturl)
    # 使用BeautifulSoup
    # soup=BeautifulSoup(r.text,"html.parser")
    ##r1 = soup.findAll('td', attrs = {'class': 'icn'})
    # urls=[pre_url+x.a['href'] for x in r1 if x.find('a')]
    # for x in r1:
    #     if x.find('a'):
    #         url=pre_url+x.a['href']

    # r0=soup.find('tbody',id=re.compile('normalthread.*'))
    # r1=r0.find('span',attrs = {'class': 'xi1'})
    # cur=time.mktime(time.strptime(r1.text,'%Y-%m-%d'))


    # 使用re正则匹配
    import re
    p=re.compile('<td class="icn">[\s]*<a href="(.*?)"')
    # urls=[pre_url+x for x in p.findall(r.text)]
    urls=p.findall(r.text)
    for x in urls:
        if x==lasturl:
            break
        tmp=pre_url+utils.quote_url(x)
        rq.put(tmp)
        print(tmp)
    lasturl=urls[0]
print(int(time.time())-t_start)