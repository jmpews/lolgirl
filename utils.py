#-*-encoding:utf-8-*-
__author__ = 'jmpews'
import requests
from logger import initLogging
import re
import time
import json
loggg=initLogging('utils.log')
from bs4 import BeautifulSoup

def quote_url(url):
    quotes={'&gt;':'>','&lt;':'<','&amp;':'&','&quot;':'\"','&#39;':'\'','&nbsp;':' '}
    for k in quotes:
        url=url.replace(k,quotes[k])
    return url


def getinfo(nickname,area):
    # 测试发现beautifulsoup比re要快,前提是已经格式化完毕
    pre_url='http://lolbox.duowan.com/'
    url=pre_url+'playerDetail.php?serverName='+area+'&playerName='+nickname
    id_info={'nickname':nickname,'area':area}
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    avatar=soup.find('div',attrs={'class':'avatar'})
    # 角色长时间不玩
    if avatar is None:
        return None
    # 角色登记太低
    if int(avatar.em.text)<11:
        return None

    # 最近战斗信息
    matchlists=[]
    matchlist=soup.find('div',attrs={'class':'recent bd-r fl'})
    matchs=matchlist.findAll('tr')[1:]
    for x in matchs:
        td=x.findAll('td')
        timestr='2015-'+td[3].text.strip()
        times=time.mktime(time.strptime(timestr,'%Y-%m-%d %H:%M'))
        # 距离上次游戏超过一个月
        if times+30*24*3600<time.time():
            return None
        matchlists.append([td[0].img['title'],td[2].text,times])

    # 战斗力,通过战斗力判断角色的选区
    fighting=soup.find('div',attrs={'class':'fighting'})
    fighting=fighting.find('span').text
    id_info['fighting']=int(fighting)

    # 常用英雄
    com_hero=soup.find('ul',id='com-hero')
    com_hero=[x['champion-name-ch'] for x in com_hero.findAll('li')]
    # re版本
    # p=re.compile('champion-name-ch="(.+?)"')
    # com_hero=p.findall(com_hero.decode())
    com_hero=com_hero[0:3] if len(com_hero)>=3 else com_hero
    id_info['com_hero']=com_hero

    # 获取段位
    r1=requests.get(url.replace('playerDetail','ajaxGetWarzone'))
    r1json=r1.json()
    if r1json['tier']!=None:
        id_info['warzone']=r1json['tier']+r1json['rank']
    else:
        id_info['warzone']=None


    # re版本
    # p=re.compile('title="(\S+?)"[\s\S]+?<em class="(?:red|green)"(\S+?)</em></td>\s<td>(.+?)</td>')
    # matchlists.append(p.findall(matchlist.decode()))
    id_info['matchlist']=matchlists
    return id_info
# getinfo('戴帽子的鼠','网通一')

# 1.验证ID是否有效
# 2.对比所有大区的角色,找到最适合的角色
def checkid(nickname,area=None):
    pre_url='http://lolbox.duowan.com/'
    qurl='http://lolbox.duowan.com/playerList.php?keyWords=%s' % (nickname)
    # 做好超时处理
    try:
        r=requests.get(qurl,timeout=4)
    except Exception as e:
        loggg.error('查询超时: '+nickname+str(e))
        # import traceback
        # traceback.print_exc()
        print('================查询超时 异常======================')
        return False
    if r.text.find('没有找到匹配用户')!=-1:
        loggg.error('ID error:'+nickname)
        print('================ID 异常======================')
        return False

    # 指定大区,但是可能指定错误
    if area!=None:
        if r.text.find(area)!=-1:
            return getinfo(pre_url+'playerDetail.php?serverName='+area+'&playerName='+nickname)

    # 没有指定大区,需要对比所有目标大区
    p=re.compile('<td >\S+? (\S{3})</td>')
    id_info={'fighting':-1}
    for area in p.findall(r.text):
        tempinfo=getinfo(nickname,area)
        if tempinfo is not None:
            if tempinfo['fighting']>id_info['fighting']:
                id_info=tempinfo
    return id_info

# checkid('戴帽子的鼠')


