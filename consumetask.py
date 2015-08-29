__author__ = 'jmpews'

import re
import json

from bs4 import BeautifulSoup
import requests

from lolgirl.redisq import RedisQueue
from threadpools import ThreadPool

rq_page=RedisQueue('girlpage')
rq_info=RedisQueue('girlinfo')
testurl='http://bbs.duowan.com/forum.php?mod=viewthread&tid=43501017&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D3317%26typeid%3D3317%26orderby%3Ddateline'
def func():
    girlurl=rq_page.get()
    r=requests.get(girlurl)
    soup=BeautifulSoup(r.text,"html.parser")
    girlpage=soup.find('td',id=re.compile('postmessage.*'),attrs={'class':'t_f'})

    IDkeys=['ID','id']
    Zonekeys={'电一':'艾欧尼亚','艾欧尼亚':'艾欧尼亚','电二':'祖安','电三':'诺克萨斯','诺克萨斯':'诺克萨斯','电六':'战争学院','战争学院':'战争学院','电四':'班德尔城','班德尔城':'班德尔城','电五':'皮尔特沃夫','皮尔特沃夫':'皮尔特沃夫','巨神峰':'巨神峰'}
    # class LolGirl(object)
    p=re.compile('(?:id|ID)[\s|:|：|;|；]*(\S+)\s+')
    girlpagetext=girlpage.text
    id=p.findall(girlpagetext)
    def checkid(id):
        qurl='http://x.15w.com/json.php?tn=search&q=%s' % (id)
        r=requests.get(qurl)
        result_code=eval(r.text[:-1])
        if result_code['code']==1:
            return False
        return True

    if len(id)>=1:
        id=id[0]
        if not checkid(id):
            return
        print(id)
        girlinfo={}
        girlinfo['id']=id
        # pickle
        rq_info.put(json.dumps(girlinfo,ensure_ascii=False))

threadpool=ThreadPool(func=func)
threadpool.start()

