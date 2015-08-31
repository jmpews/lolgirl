__author__ = 'jmpews'

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


