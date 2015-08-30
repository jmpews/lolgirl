__author__ = 'jmpews'

def quote_url(url):
    quotes={'&gt;':'>','&lt;':'<','&amp;':'&','&quot;':'\"','&#39;':'\'','&nbsp;':' '}
    for k in quotes:
        url=url.replace(k,quotes[k])
    return url