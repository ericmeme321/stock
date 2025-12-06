# -*- coding: utf-8 -*-
from re import template
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

# 可選套件
try:
    from fake_useragent import UserAgent
    HAS_FAKE_UA = True
except ImportError:
    HAS_FAKE_UA = False


# d = ['Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)'
#     , 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
#     , 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)'
#     , 'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00'
#     , 'Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01'
#     , 'Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10'
#     , 'Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00'
#     , 'Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62']

def Get_Now():
    """獲取當前時間戳"""
    Today_Time = datetime.datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    Today_Time_Stamp = time.strptime(Today_Time, "%Y-%m-%d-%H-%M-%S")
    return Today_Time_Stamp

def Get_Now_Plus():
    """獲取最近交易日的時間戳（排除週末）"""
    day = datetime.datetime.today().isoweekday()
    if day == 6:  # 星期六
        reduce = -1
    elif day == 7:  # 星期日
        reduce = -2
    else:
        reduce = 0

    Today_Time = (datetime.datetime.today() + datetime.timedelta(days=reduce)).strftime("%Y-%m-%d")
    Today_Time_Array = time.strptime(Today_Time, "%Y-%m-%d")
    Today_Time_Stamp = int(time.mktime(Today_Time_Array)) * 1000
    print(f'[資訊] 使用日期時間戳: {Today_Time_Stamp} ({Today_Time})')

    return Today_Time_Stamp

def Get_Latest_Trading_Date():
    """獲取最近的交易日（YYYYMMDD格式）"""
    day = datetime.datetime.today().isoweekday()
    if day == 6:  # 星期六，回到星期五
        reduce = -1
    elif day == 7:  # 星期日，回到星期五
        reduce = -2
    else:
        reduce = 0

    latest_date = (datetime.datetime.today() + datetime.timedelta(days=reduce)).strftime("%Y%m%d")
    return latest_date

def Get_Date_Range(days_back=30):
    """
    獲取日期範圍
    Args:
        days_back: 往前推幾天，預設30天
    Returns:
        (start_date, end_date) 格式為 YYYYMMDD
    """
    end_date = Get_Latest_Trading_Date()
    start_date = (datetime.datetime.today() - datetime.timedelta(days=days_back)).strftime("%Y%m%d")
    return start_date, end_date

def crawler(url, max_retries=3):
    """
    改進的爬蟲函數
    Args:
        url: 要爬取的網址
        max_retries: 最大重試次數，預設為3次
    Returns:
        JSON資料或None
    """
    time.sleep(3)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    }

    for retry_count in range(max_retries):
        try:
            session = requests.Session()
            res = session.get(url, headers=headers, timeout=10)

            if res.status_code == 200:
                res.encoding = 'utf-8'
                print(f'[成功] 狀態碼: {res.status_code}')
                print(f'[URL] {url}')
                return json.loads(res.text, strict=False)
            else:
                print(f'[警告] 狀態碼: {res.status_code}, 重試 {retry_count + 1}/{max_retries}')
                print(f'[URL] {url}')
                time.sleep(random.randint(3, 5))

        except requests.exceptions.Timeout:
            print(f'[逾時] 連線逾時，重試 {retry_count + 1}/{max_retries}')
            time.sleep(random.randint(3, 5))

        except requests.exceptions.RequestException as e:
            print(f'[錯誤] 網路請求錯誤: {e}, 重試 {retry_count + 1}/{max_retries}')
            time.sleep(random.randint(3, 5))

        except json.JSONDecodeError as e:
            print(f'[錯誤] JSON 解析失敗: {e}')
            return None

        except KeyboardInterrupt:
            print('[中斷] 使用者中斷程式')
            sys.exit(1)

    print(f'[失敗] 已達最大重試次數 {max_retries}，放棄爬取')
    return None

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