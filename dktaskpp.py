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



def func():
    girlid=rq_girl.get().decode()
    girlid=json.loads(girlid)
    idinfo_15w= utils.checkid(girlid['nickname'])
    if not idinfo_15w:
        return
    overinfo=utils.overdate(idinfo_15w['player'])
    if not overinfo:
        return

    girlinfo={}
    girlinfo['picurls']=[girlid['picurl']]
    girlinfo['nickname']=girlid['nickname']
    girlinfo.update(idinfo_15w)
    girlinfo.update(overinfo)
    print(girlinfo)
    # pickle也可以作序列化
    rq_info.put(json.dumps(girlinfo,ensure_ascii=False))


# 建立线程池
threadpool=ThreadPool(func=func)
threadpool.start()