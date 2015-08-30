__author__ = 'jmpews'

import re
import json

import utils

from bs4 import BeautifulSoup
import requests

from redisq import RedisQueue
from threadpools import ThreadPool

rq_girl=RedisQueue('dwgirl')
rq_info=RedisQueue('girlinfo')
testurl='http://bbs.duowan.com/forum.php?mod=viewthread&tid=43501017&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D3317%26typeid%3D3317%26orderby%3Ddateline'


def func():
    # 找到第一篇帖子内容
    girlurl=rq_girl.get()
    r=requests.get(girlurl)
    soup=BeautifulSoup(r.text,"html.parser")
    girlpage=soup.find('td',id=re.compile('postmessage.*'),attrs={'class':'t_f'})

    IDkeys=['ID','id']
    # Zonekeys={'电一':'艾欧尼亚','艾欧尼亚':'艾欧尼亚','电二':'祖安','电三':'诺克萨斯','诺克萨斯':'诺克萨斯','电六':'战争学院','战争学院':'战争学院','电四':'班德尔城','班德尔城':'班德尔城','电五':'皮尔特沃夫','皮尔特沃夫':'皮尔特沃夫','巨神峰':'巨神峰'}
    # 提取妹纸id
    p=re.compile('(?:id|ID)[\s|:|：|;|；]*(\S+)\s+')
    girlpagetext=girlpage.text
    id=p.findall(girlpagetext)

    # 检查id是否存在
    def checkid(id):
        qurl='http://x.15w.com/json.php?tn=search&q=%s' % (id)
        r=requests.get(qurl)
        rj=json.loads(r.text[1:-2])
        if rj['code']==1:
            return False
        rjsarray=rj['data']
        maxrj=rjsarray[0]
        for x in rjsarray[1:]:
            if x['level']>maxrj['level']:
                maxrj=x
            if x['tier']<maxrj['tier']:
                maxrj=x
        return {'tier_name':maxrj['tier_name'],'area_id':maxrj['area_id'],'area_name':maxrj['area_name'],'palyer':maxrj['player']}

    # 判断是否存在id关键字
    if len(id)<1:
        return
    # 判断有没有照片
    pics=girlpage.find_all('img',zoomfile=True)
    if len(pics)<1:
        return

    id=id[0]
    idinfo_15w= checkid(id)
    if not idinfo_15w:
        return
    girlinfo={}
    girlinfo['id']=id

    # 保存来自15w的id信息
    girlinfo.update(idinfo_15w)

    # 保存图片url
    if len(pics)>2:
        pics=pics[:2]
    piclist=[utils.quote_url(pic.attrs['zoomfile']) for pic in pics]
    girlinfo['picurls']=piclist

    print(girlinfo)
    # pickle也可以作序列化
    rq_info.put(json.dumps(girlinfo,ensure_ascii=False))

# 建立线程池
threadpool=ThreadPool(func=func)
threadpool.start()

