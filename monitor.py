__author__ = 'jmpews'
def monitor_redis(rediss=['girlinfo']):
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
        time.sleep(5)

monitor_redis()