__author__ = 'jmpews'

import re
import json
import time

from bs4 import BeautifulSoup
import requests

from redisq import RedisQueue
from threadpools import ThreadPool

from logger import initLogging
import utils

rq_girl=RedisQueue('dwgirl')
rq_info=RedisQueue('girlinfo')

testurl='http://bbs.duowan.com/forum.php?mod=viewthread&tid=43589034&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D3317%26typeid%3D3317%26orderby%3Ddateline'
loggg=initLogging('dwtaskpp.log')

# 重视模块化
# 重视模块重用
def func():
    # 找到第一篇帖子内容
    # 多玩帖子内需要特别判断的函数,比如是否存在ID关键字,以及是否存在图片.
    def duowanfunc():
        girlurl=rq_girl.get()
        r=requests.get(girlurl)
        soup=BeautifulSoup(r.text,"html.parser")
        # girlpage=soup.find('td',id=re.compile('postmessage.*'),attrs={'class':'t_f'})
        girlpage=soup.find('div',attrs={'class':'t_fsz'})
        if not girlpage:
            return
        IDkeys=['ID','id']
        # 提取妹纸id
        p=re.compile('(?:id|ID)[\s|:|：|;|；]*(\S+)\s*')
        girlpagetext=girlpage.text
        nickname=p.findall(girlpagetext)

        # 判断是否存在id关键字
        if len(nickname)<1:
            return False
        # 判断有没有照片
        pics=girlpage.find_all('img',zoomfile=True)

        if len(pics)<1:
            return False
        nickname=nickname[0]

        # 保存图片url
        if len(pics)>5:
            pics=pics[:5]
        piclist=[utils.quote_url(pic.attrs['zoomfile']) for pic in pics]
        return {'nickname':nickname,'picurls':piclist}


    duowaninfo=duowanfunc()
    if not duowaninfo:
        return
    # 通用检查id是否存在
    idinfo_15w= utils.checkid(duowaninfo['nickname'])
    if not idinfo_15w:
        return
    overinfo=utils.overdate(idinfo_15w['player'])
    if not overinfo:
        return

    girlinfo={}

    girlinfo.update(idinfo_15w)
    girlinfo.update(overinfo)
    girlinfo.update(duowaninfo)

    print(girlinfo)
    # pickle也可以作序列化
    rq_info.put(json.dumps(girlinfo,ensure_ascii=False))

# 建立线程池
threadpool=ThreadPool(func=func)
threadpool.start()
# func()
