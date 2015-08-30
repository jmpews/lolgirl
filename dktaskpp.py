__author__ = 'jmpews'



import time
from threadpools import ThreadPool
import requests
import utils
from redisq import RedisQueue
import json
import pickle
t_start=int(time.time())

rq_girl=RedisQueue('dkgirl')
rq_info=RedisQueue('girlinfo')


def checkid(id,area_name):
    qurl='http://x.15w.com/json.php?tn=search&q=%s' % (id)
    r=requests.get(qurl)
    rj=json.loads(r.text[1:-2])
    if rj['code']==1:
        return False
    rjsarray=rj['data']
    for r in rjsarray:
        if r['area_name']==area_name:
            return {'tier_name':r['tier_name'],'area_id':r['area_id'],'area_name':r['area_name'],'palyer':r['player']}
    return False

def func():
    girlid=rq_girl.get().decode()
    girlid=json.loads(girlid)
    idinfo_dk=checkid(girlid['id'],girlid['area_name'])
    print(idinfo_dk)
    if not idinfo_dk:
        return
    girlinfo={}
    girlinfo['picurls']=[girlid['picurl']]
    girlinfo.update(idinfo_dk)
    print(girlinfo)
    # pickle也可以作序列化
    rq_info.put(json.dumps(girlinfo,ensure_ascii=False))


# 建立线程池
threadpool=ThreadPool(func=func)
threadpool.start()