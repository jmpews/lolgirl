__author__ = 'jmpews'

import time

import requests
import utils
from redisq import RedisQueue

pre_url=r"http://bbs.duowan.com/"
purl="http://bbs.duowan.com/forum.php?mod=forumdisplay&fid=1343&orderby=dateline&typeid=3317&orderby=dateline&typeid=3317&filter=author&page=%s"


t_start=int(time.time())
rq=RedisQueue('dwgirl')

i=0
while True:
    i=i+1
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
        rq.put(pre_url+utils.quote_url(x))
print(int(time.time())-t_start)