__author__ = 'jmpews'

import time

import requests

from redisq import RedisQueue

pre_url=r"http://bbs.duowan.com/"
purl="http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1343&orderby=dateline&typeid=3317&orderby=dateline&typeid=3317&filter=author&page=%s"
def quote_url(url):
    quotes={'&gt;':'>','&lt;':'<','&amp;':'&','&quot;':'\"','&#39;':'\'','&nbsp;':' '}
    for k in quotes:
        url=url.replace(k,quotes[k])
    return url

t_start=int(time.time())
rq=RedisQueue('girlpage')

for i in range(1,2):
    requesturl=purl % (i)
    r=requests.get(requesturl)

    # 使用BeautifulSoup
    # soup=BeautifulSoup(r.text,"html.parser")
    # r1 = soup.findAll('td', attrs = {'class': 'icn'})
    # urls=[pre_url+x.a['href'] for x in r1 if x.find('a')]
    # print(urls)

    # 使用re正则匹配
    import re
    p=re.compile('<td class="icn">[\s]*<a href="(.*?)"')
    # urls=[pre_url+x for x in p.findall(r.text)]
    for x in p.findall(r.text):
        rq.put(pre_url+quote_url(x))
print(int(time.time())-t_start)