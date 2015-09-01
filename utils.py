__author__ = 'jmpews'

import requests
from logger import initLogging
import re
import time
import json
loggg=initLogging('utils.log')


def quote_url(url):
    quotes={'&gt;':'>','&lt;':'<','&amp;':'&','&quot;':'\"','&#39;':'\'','&nbsp;':' '}
    for k in quotes:
        url=url.replace(k,quotes[k])
    return url

def monitor_redis(rediss):
    import time
    from redisq import RedisQueue
    print('start monitor...')
    rqs=[]
    for x in rediss:
        rqs.append(RedisQueue(x))
    while True:
        for x in rqs:
            print(x.qsize())
        print('-------------')
        time.sleep(10)


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