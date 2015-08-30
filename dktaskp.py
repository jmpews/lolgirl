__author__ = 'jmpews'
__author__ = 'jmpews'



import time
import requests
import utils
from redisq import RedisQueue
import json
import pickle
t_start=int(time.time())

rq=RedisQueue('dkgirl')

girlurl='http://api.gz.1251328275.cee.myqcloud.com/pic.php?s=m&sort=new&p=1'



lasttime=int(time.time())-3600*24
while True:
    print('one loop...')
    r=requests.get(girlurl)
    rjson=json.loads(r.text[1:-1])
    ids=[]
    print(rjson)
    for x in rjson:
        if x['created_at']<=lasttime:
            break
        if x['game_id'] in ids:
            continue
        ids.append(x['game_id'])
        info={'id':x['game_id'],'area_name':x['server'],'picurl':x['photo_url']}
        print(info)
        # pickle也可以作序列化
        rq.put(json.dumps(info,ensure_ascii=False))
    if len(rjson)>0:
        lasttime=rjson[0]['created_at']
    time.sleep(5)

