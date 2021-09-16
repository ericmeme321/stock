from often import *

def Get_Market_Data():
    Now_Time = Get_Now_Plus()
    num = 60
    # num = input("資料筆數 :")

    All_Market_Data_URL = f'https://www.wantgoo.com/investrue/0000/historical-daily-candlesticks?before={Now_Time}&top={num}'

    Market_Data = crawler(All_Market_Data_URL)

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

    Market_Df = pd.DataFrame(idx)

    for c in Market_Data:
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
        Market_List = []

        Temp_List.extend([ratio, open, high, low, close, up, mid, down])
        Temp_List = Display_Two_Decimal_Place(Temp_List)
        Temp_List.insert(0, String_Time)
        Temp_List.append(vol)
        Market_List.extend(Temp_List)
        

        Market_Df_len = len(Market_Df)
        Market_Df.loc[Market_Df_len] = Market_List

    Market_Df['成交量'] = Market_Df['成交量'].astype(int)
    Market_Df['漲跌幅'] = Market_Df['漲跌幅'].shift(-1)
    Market_Df['漲跌幅'] = round((Market_Df['收盤價'] - Market_Df['漲跌幅']) / Market_Df['漲跌幅'] * 100, 2)
    Market_Df = Market_Df[:len(Market_Df)-1]
    print(Market_Df)
    print()

    # Market_df.to_csv('C:/temp/Market_'+date+'.csv',encoding='utf_8_sig', header=True)

    return Market_Df

def Get_Market_Minute_Data():
    # Search_Time = input("日期(例:20210511) : ")
    # Search_Time_Stamp = Get_Search_Time_Stamp(Search_Time)
    Search_Time_Stamp = Get_Now_Plus()
    Market_Minute_Data_URL = f'https://www.wantgoo.com/investrue/0000/historical-realtimeprice-tradedate?tradeDate={Search_Time_Stamp}&k=MjUwMDMyMzM5MDkzODY3NzIwMDAw'
    
    Temp_Data = crawler(Market_Minute_Data_URL)
    Market_Minute_Data = Temp_Data['data']

    idx = {'日期':[],
            '最高價':[],
            '最低價':[],
            '收盤價':[],
            '成交量':[],}

    Market_Minute_Df = pd.DataFrame(idx)
    

    for c in Market_Minute_Data:
        t = c['time']

        Struct_Time = time.localtime(t/1000)
        String_Time = time.strftime("%H:%M", Struct_Time)       
        close = c['close']
        high = c['high']
        low = c['low']
        vol = c['volume']

        Temp_List = []
        Market_Minute_List = []

        Temp_List.extend([high, low, close])
        Temp_List = Display_Two_Decimal_Place(Temp_List)
        
        Market_Minute_List.append(String_Time)
        Temp_List.append(vol)
        Market_Minute_List.extend(Temp_List)


        Market_Minute_Df_len = len(Market_Minute_Df)
        Market_Minute_Df.loc[Market_Minute_Df_len] = Market_Minute_List

    Market_Minute_Df['成交量'] = Market_Minute_Df['成交量'].astype(int)
    print(Market_Minute_Df)

    return Market_Minute_Df