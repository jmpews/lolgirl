__author__ = 'jmpews'
import redis

class RedisQueue(object):
    def __init__(self,name,namespace='queue',**redis_kwargs):
        self.__db=redis.StrictRedis(host='linevery.com', port=6379, db=0)
        self.key = '%s:%s' % (name,namespace)

    def qsize(self):
        return self.__db.llen(self.key)

    def qrange(self,start,end):
        return self.__db.lrange(self.key,start,end)

    def empty(self):
        return self.qsize()==0

    def index(self,i):
        return self.__db.lindex(self.key,i)
