#!/usr/bin/env python
# coding: utf-8

import urllib.request
import time
import pandas as pd
import numpy as np
from datetime import datetime



Date = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y')
pin = ["382481","380061","380013","380009"]

ans=""
ans+="\tVACCINE SLOTS REPORT\n"
ans+="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

ans+=f"Last Update : {datetime.fromtimestamp(time.time()).strftime('%HH-%MM : %d-%m-%Y')}\n\n"

for k in pin:
    ans+="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    ans+=f"\t{k}\n"
    ans+="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={k}&date={Date}"
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    Data = pd.read_json(data)
    for i in Data["centers"]:
        ans+=i["name"]+"\n"
        for j in i["sessions"]:
            if j["min_age_limit"]==18:
                ans+=f"{j['date']} : {j['available_capacity']} : {j['min_age_limit']}+\n"
                if int(j['available_capacity'])>1:
                    from pushbullet import Pushbullet
                    f = open("API_KEY.txt")
                    APIKEY = f.read()
                    f.close()
                    pb = Pushbullet(APIKEY)
                    push = pb.push_note(f"{j['available_capacity']} seats available", f"Location: {i['name']}, {k}")            
        ans+="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
print(ans)
