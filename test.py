__author__ = 'jmpews'
import requests
def proxy_req(func):
    def _wrapper(*args,**kwargs):
        r=func(*args,**kwargs)
        print('wrap success...')
        return r
    return _wrapper()

@proxy_req()

def proxy_get():
    pass
