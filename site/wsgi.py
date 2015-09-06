__author__ = 'jmpews'

import tornado.web
import tornado.ioloop
import tornado.gen

import json
import utils
import os
import time

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
        t=random.randint(1,9000)
        girls=rq.qrange(t,t+11)
        girlslist=[]
        matchlist=[]
        for x in girls:
            girl=json.loads(x.decode())
            tmp=[]
            for y in girl['matchlist']:
                # tmp.append(y[0]+' · '+y[1]+' · '+time.strftime('%m-%d %H:%M',time.localtime(y[2])))
                classtype='lose' if y[1]=='失败' else 'win'
                tmp.append([y[0]+' ● '+y[1]+' ● '+time.strftime('%m-%d %H:%M',time.localtime(y[2])),classtype])
            lastime=girl['matchlist'][0][2]
            lastime =time.strftime('%Y-%m-%d %H:%M',time.localtime(lastime))
            girlslist.append([girl['nickname'],girl['area'],girl['warzone'],tmp,lastime])
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

tier_name={'不屈白银':'silver','荣耀黄金':'gold','华贵铂金':'platinum'}

application=tornado.web.Application(handlers=handlers,**settings)
rq=utils.RedisQueue('girlinfo')

application.listen(8087)
print('listening 8087...')
tornado.ioloop.IOLoop.current().start()