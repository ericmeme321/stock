from often import *

def Get_Cash_Flow():
    Cash_Flow_Data_URL = f'https://pscnetsecrwd.moneydj.com/b2brwdCommon/jsondata/c6/fb/f2/twstockdata.xdjjson?x=afterhours-market0003-1&revision=2018_07_31_1'
    
    Temp_Data = crawler(Cash_Flow_Data_URL)

    Cash_Flow_Data = Temp_Data['ResultSet']

    comment = Cash_Flow_Data['Comment']

    Cash_Flow_Data = Cash_Flow_Data['Result']

    print(comment)

    idx = {'產業類股':[],
            '今日成交值(億)':[],
            '昨日成交值(億)':[],
            '差值(億)':[],}

    Cash_Flow_Data_Df = pd.DataFrame(idx)

    Sum_Cash = 0
    for c in Cash_Flow_Data:
        industy = c['V4']
        Today_Amount = float(c['V5']) / 100000
        Yesturday_Amount = float(c['V6']) / 100000
        deviation = Today_Amount - Yesturday_Amount

        if industy == '加權指數':
            break

        Temp_List = [Today_Amount, Yesturday_Amount, deviation]
        Temp_List = Display_Two_Decimal_Place(Temp_List)
        
        Sum_Cash += Today_Amount
        Cash_Flow_Data_List = []
        Cash_Flow_Data_List.extend([industy, Temp_List[0], Temp_List[1], Temp_List[2]])

        
        Cash_Flow_Data_Df_len = len(Cash_Flow_Data_Df)
        Cash_Flow_Data_Df.loc[Cash_Flow_Data_Df_len] = Cash_Flow_Data_List
    
    # print(Sum_Cash,Today_Amount)

    print(Cash_Flow_Data_Df)
    print

    return Cash_Flow_Data_Df