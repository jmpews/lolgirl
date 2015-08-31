__author__ = 'jmpews'

import re
import json
import time
import utils

from bs4 import BeautifulSoup
import requests

from redisq import RedisQueue
from threadpools import ThreadPool

from logger import initLogging

rq_girl=RedisQueue('dwgirl')
rq_info=RedisQueue('girlinfo')

testurl='http://bbs.duowan.com/forum.php?mod=viewthread&tid=43589034&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D3317%26typeid%3D3317%26orderby%3Ddateline'
loggg=initLogging('dwtaskpp.log')

# 重视模块化
# 重视模块重用
def func():
    # 找到第一篇帖子内容
    # 检查id是否存在
    def checkid(nickname):
    # 1.验证ID是否有效
        qurl='http://x.15w.com/json.php?tn=search&q=%s' % (nickname)
        try:
            r=requests.get(qurl,timeout=4)
        except Exception as e:
            loggg.error(e)
            import traceback
            # traceback.print_exc()
            print('================ID 异常======================')
            return False
        if r.text.find('code')==-1:
            return False

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
        return {'tier_name':maxrj['tier_name'],'area_id':maxrj['area_id'],'area_name':maxrj['area_name'],'player':maxrj['player']}

    def overdate(player):
        # 2.验证ID是否长时间不使用
        #   查询近期战绩
        battleurl='http://x.15w.com/battle/%s' % (player)
        try:
            r=requests.get(battleurl)
        except Exception as e:
            import traceback
            traceback.print_exc()
            loggg.error(e)
            print('================ID 异常======================')
        p=re.compile(r'"battle_time":(\d+)')
        battletimes=p.findall(r.text)
        tmpsum=0
        battlelist=[]
        for tmp in battletimes:
            tmpsum+=int(tmp)
            battlelist.append(int(tmp))
        # 判断防止异常
        if len(battletimes)==0:
            return False
        # 距离上一次玩的平均时间超过1一个月,表明不在活跃
        overtime=int(time.time())-tmpsum/len(battletimes)
        if overtime > 15*3600*24:
            print('================ID 过期======================')
            return False
        return {'battletimes':battlelist}
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
        print(nickname)
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
    idinfo_15w= checkid(duowaninfo['nickname'])
    if not idinfo_15w:
        return
    overinfo=overdate(idinfo_15w['player'])
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
