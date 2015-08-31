__author__ = 'jmpews'

import re
import requests
import time

def func():
    battle='http://x.15w.com/champions/1rihx6n54iggx3pfe6d'
    r=requests.get(battle)
    p=re.compile(r'"battle_time":(\d+)')
    battletimes=p.findall(r.text)
    tmpsum=0
    for ti in battletimes:
        tmpsum+=int(ti)
    inter=int(time.time())-tmpsum/len(battletimes)