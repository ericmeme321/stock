from re import search
from often import *

def Get_Stock_sets(Stock_Name,Now_Time):
    Stock_Set_URL = f'https://www.wantgoo.com/investrue/{Stock_Name}/historical-topfivepieces?v={Now_Time}'
    Stock_Set_Data = crawler(Stock_Set_URL)

    
    Sell = Stock_Set_Data['dealOnBidPrice']
    Buy = Stock_Set_Data['dealOnAskPrice']

    Sell_Radio = Sell / (Sell + Buy) * 100
    Buy_Radio = 100 - Sell_Radio

    Sell_Radio = round(Sell_Radio, 0)
    Buy_Radio = round(Buy_Radio, 0)

    print("內盤數量 :",Sell," 外盤數量 :",Buy)
    print("內盤比 : 外盤比 = ",Sell_Radio,":",Buy_Radio)
    print()

    return Stock_Set_Data

def Get_Stock_Data(Stock_Name):
    Now_Time = Get_Now_Plus()
    # num = input('資料筆數 : ')

    All_Stock_Data_URL = f'https://www.wantgoo.com/investrue/{Stock_Name}/historical-daily-candlesticks?before={Now_Time}&top=60'

    # Stock_Sets = Get_Stock_sets(Stock_Name, Now_Time)

    Stock_Data = crawler(All_Stock_Data_URL)

    idx = {'日期':[],
                '漲跌幅':[],
                '開盤價':[],
                '最高價':[],
                '最低價':[],
                '收盤價':[],
                '上關價':[],
                '中關價':[],
                '下關價':[],
                '成交量':[],}

    Stock_Df = pd.DataFrame(idx)

    for c in Stock_Data:
        t = c['time']

        Struct_Time = time.localtime(t/1000)
        String_Time = time.strftime("%Y/%m/%d", Struct_Time)

        ratio = c['close']
        open = c['open']
        close = c['close'] 
        high = c['high']
        low = c['low']
        vol = c['volume']

        up, mid, down = Calculate_Up_AND_Mid_AND_Down(high, low)

        # pricing, ratio = Get_Pricing_AND_Ratio(Today_Close, Yesturday_Close)


        Temp_List = []
        Stock_List = []

        Temp_List.extend([ratio, open, high, low, close, up, mid, down])
        Temp_List = Display_Two_Decimal_Place(Temp_List)

        # pricing,ratio = Temp_List[0], Temp_List[1]
        # del Temp_List[0:2]

        # Stock_List.extend([String_Time,str(pricing) + ' (' + str(ratio) + '%)'])
        Temp_List.insert(0, String_Time)
        Temp_List.append(vol)
        Stock_List.extend(Temp_List)

        Stock_Df_len = len(Stock_Df)
        Stock_Df.loc[Stock_Df_len] = Stock_List

    Stock_Df['漲跌幅'] = Stock_Df['漲跌幅'].shift(-1)
    Stock_Df['漲跌幅'] = round((Stock_Df['收盤價'] - Stock_Df['漲跌幅']) / Stock_Df['漲跌幅'] * 100, 2)
    Stock_Df = Stock_Df[:len(Stock_Df)-1]

    print(Stock_Df)
    print()

    # Show_Cadlestick_Chart(Stock_Df)
    # Stock_df.to_csv('C:/temp/'+stock_name+'_'+date+'.csv',encoding='utf_8_sig', header=True)


    return Stock_Df

def Get_Stock_Minute_Data(Stock_Name):
    # Search_Time = input("日期(例:20210511) : ")
    # Search_Time_Stamp = Get_Search_Time_Stamp(Search_Time)
    Search_Time_Stamp = Get_Now_Plus()
    Stock_Minute_Data_URL = f'https://www.wantgoo.com/investrue/{Stock_Name}/historical-realtimeprice-tradedate?tradeDate={Search_Time_Stamp}&k=MjUwMDMyMzM5MDkzODY3NzIwMDAw'
    Temp_Data = crawler(Stock_Minute_Data_URL)
    Stock_Minute_Data = Temp_Data['data']


    idx = {'日期':[],
            '最高價':[],
            '最低價':[],
            '收盤價':[],
            '成交量':[],}

    Stock_Minute_Df = pd.DataFrame(idx)
    

    for c in Stock_Minute_Data:
        t = c['time']

        Struct_Time = time.localtime(t/1000)
        String_Time = time.strftime("%H:%M", Struct_Time)       
        close = c['close']
        high = c['high']
        low = c['low']
        vol = c['volume']

        Temp_List = []
        Stock_Minute_List = []

        Temp_List.extend([high, low, close])
        Temp_List = Display_Two_Decimal_Place(Temp_List)
        
        Stock_Minute_List.append(String_Time)
        Temp_List.append(vol)
        Stock_Minute_List.extend(Temp_List)


        Market_Minute_Df_len = len(Stock_Minute_Df)
        Stock_Minute_Df.loc[Market_Minute_Df_len] = Stock_Minute_List

    Stock_Minute_Df['成交量'] = Stock_Minute_Df['成交量'].astype(int)
    print(Stock_Minute_Df)

    return Stock_Minute_Df

def Get_Stock_information(Stock_Name):
    # Search_Time = input("日期(例:20210511) : ")
    # Search_Time_Stamp = Get_Search_Time_Stamp(Search_Time)
    Stock_Data_URL = f'https://isin.twse.com.tw/isin/single_main.jsp?owncode={Stock_Name}&stockname='
    headers = {'User-Agent': 'Mozilla/5.0'}
    while 1:
        try:
            session = requests.Session()
            res =  session.get(Stock_Data_URL, headers=headers, timeout=5)
            if res.status_code != 200:
                time.sleep(random.randint(3,5))
                print(res.status_code)
                print(Stock_Data_URL)
            else:
                res.encoding = 'big5'
                print(res.status_code)
                Temp_Data = res.text
                break
        except Exception as e:
            print(e)
            time.sleep(random.randint(3,5))
            continue
        
    print(Temp_Data)
    return