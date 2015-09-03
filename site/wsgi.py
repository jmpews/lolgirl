__author__ = 'jmpews'

import tornado.web
import tornado.ioloop
import tornado.gen

import json
import utils

import os

class AsyncMainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        print('client come...')
        yield tornado.gen.sleep(3)
        print('wake...')
        self.write('hello world...')

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print('client come...')
        import random
        t=random.randint(100,4000)
        girls=rq.qrange(t,t+10)
        girlslist=[]
        for x in girls:
            girl=json.loads(x.decode())
            print(girl)
            i=random.randint(1,4)
            girlslist.append([girl['nickname'],girl['area_name'],girl['tier_name'],i])
        self.render('index.html',girls=girlslist)

handlers=[
    (r'/',MainHandler)
]
settings={
    'autoreload':True,
    'template_path':'./templates',
    'static_path':'./statics',
    'static_url_prefix':'/cdn/'
}


application=tornado.web.Application(handlers=handlers,**settings)
rq=utils.RedisQueue('girlinfo')

application.listen(8087)
print('listening 8087...')
tornado.ioloop.IOLoop.current().start()