from re import template
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import datetime
import random
import csv
import sys
import pandas as pd
import numpy as np
import json
import requests
import time


# d = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)'
#     , 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
#     , 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)'
#     , 'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00'
#     , 'Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01'
#     , 'Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10'
#     , 'Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00'
#     , 'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62']

def Get_Now():
    Today_Time = (datetime.datetime.today()).strftime("%Y-%m-%d")
    Today_Time_Array = time.strptime(Today_Time, "%Y-%m-%d")
    Today_Time_Stamp = int(time.mktime(Today_Time_Array)) * 1000
    # Now_Time = int(time.time()) * 1000

    return Today_Time_Stamp

def Get_Now_Plus():
    day = datetime.datetime.today().isoweekday()
    if day == 6:
        reduce = -1
    elif day == 7:
        reduce = -2
    else:
        reduce = 0

    Today_Time = (datetime.datetime.today() + datetime.timedelta(days = reduce)).strftime("%Y-%m-%d")
    Today_Time_Array = time.strptime(Today_Time, "%Y-%m-%d")
    Today_Time_Stamp = int(time.mktime(Today_Time_Array)) * 1000
    # Now_Time = int(time.time()) * 1000
    print(Today_Time_Stamp)
    
    return Today_Time_Stamp

def crawler(url):
    c = 0
    time.sleep(3)
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    # ua = UserAgent()
    # uadata = ua.random
    headers = {'User-Agent': 'Mozilla/5.0',
    #    'Cookie': 'BID=68712885-7B4D-4E7D-8308-21A4A96FA0F6; _hjid=3afd2b14-71f9-4e48-b59f-e01af5167951; _ga=GA1.2.1976740203.1624471427; _smt_uid=60d37782.1655ca1d; BrowserMode=Web; _gcl_au=1.1.1702182853.1624471428; hblid=7pMrcsEHIB9oPT3I3h7B70HloBb4jLar; olfsk=olfsk4293187356974473; member_token=eyJpZCI6Mjk4Mzk4LCJ1c2VyTmFtZSI6ImVyaWNtZW1lMzIxQGdtYWlsLmNvbSIsIm5pY2tOYW1lIjoiZXJpY21lbWUzMjEiLCJoZWFkc2hvdCI6Imh0dHBzOi8vaW1nLndhbnRnb28uY29tL3dhbnRnb29maWxlcy91cGxvYWRmaWxlcy9kZWZhdWx0LW1lbWJlci1oZWFkc2hvdC5wbmcifQ..~70ba68b93dbbe6b3b374e0cc2dab7907c8ea73e931a2be6b7386d3d2de378396; popup=showed; _okdetect=%7B%22token%22%3A%2216284885737960%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.wantgoo.com%22%7D; _ok=8391-691-10-7433; idUserName=ericmeme321%40gmail.com; authorizedKey=BvW4wM%2btAFEkJXv%2fBEDFpQz%2bnbxMv8Up; UserName=BvW4wM%2btAFEkJXv%2fBEDFpQz%2bnbxMv8Up; NickName=ericmeme321; UserAccount=ericmeme321%40gmail.com; Member_No=298398; IsLogin=True; urls=m.wantgoo.com; img=https%3a%2f%2fwww.wantgoo.com%2fimage%2fdisplaydefault1.png; Email=ericmeme321%40gmail.com; AdState=Show; MemberLevel=Normal; wcsid=J0JI1XLANxjRATkK3h7B70H4UpBo6VA6; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1628494614383%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; client_signature=c7aa90d1bdb42cbcbbeff8377653e4364bef11de49da77279c7e5885c0b8de2d; _oklv=1628499322895%2CJ0JI1XLANxjRATkK3h7B70H4UpBo6VA6',
    #    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    #    'Accept-Encoding': 'none',
    #    'Accept-Language': 'en-US,en;q=0.8',
    #    'Connection': 'keep-alive'
    }
    while 1:
        try:
            session = requests.Session()
            res =  session.get(url, headers=headers, timeout=5)
            if res.status_code != 200:
                time.sleep(random.randint(3,5))
                print(res.status_code)
                print(url)
                return
            else:
                res.encoding = 'utf-8'
                print(res.status_code)
                return json.loads(res.text, strict=False)
            # with open('ip.csv','r') as f:
            #     lines = csv.reader(f)
            #     for i in lines:
            #         ip = i
            #         break
            #     for i in range(len(ip)):
            #         res =  session.get(url, headers=headers, proxies={'http':ip[i], 'https':ip[i]}, timeout=5)
            #         if res.status_code != 200:
            #             time.sleep(random.randint(3,5))
            #             print(ip[i], res.status_code)
            #             print(url)
            #         else:
            #             res.encoding = 'utf-8'
            #             print(ip[i], res.status_code)
            #             return json.loads(res.text, strict=False)
        except Exception as e:
            print(e)
            time.sleep(random.randint(3,5))
            continue
        except KeyboardInterrupt as e:
            sys.exit(1)

def Display_Two_Decimal_Place(arr):
    for i in range(0,len(arr)):
        arr[i] = round(arr[i], 2)

    return arr

def Calculate_Up_AND_Mid_AND_Down(high, low):
    up = low + (high - low) * 1.382
    mid = (high + low) / 2
    down = high - (high - low) * 1.382

    return up,mid,down

def Calculate_Price_Average(Buy_Price, Sell_Price, Buy_Quantities, Sell_Quantities):
    if Buy_Quantities + Sell_Quantities != 0:
        return (Buy_Price * Buy_Quantities + Sell_Price * Sell_Quantities) / (Buy_Quantities + Sell_Quantities)
    else:
        return 0

def Get_Pricing_AND_Ratio(Today_Close, Yesturday_Close):
    pricing = Today_Close - Yesturday_Close
    ratio = (Today_Close - Yesturday_Close) / Yesturday_Close * 100

    return pricing, ratio

def Get_Search_Time_Stamp(Search_Time):
    Search_Time_Array = time.strptime(Search_Time,"%Y%m%d")
    Search_Time_Stamp = int(time.mktime(Search_Time_Array)) * 1000

    return Search_Time_Stamp 