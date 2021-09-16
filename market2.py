from often import *

def Get_Market_Data():
    Now_Time = Get_Now()
    # num = input('資料筆數 : ')

    Market_Data_URL = f'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date=&_={Now_Time}'

    Market_Data = crawler(Market_Data_URL)


    if Market_Data['stat'] == 'OK':
        print(Market_Data['title'], Market_Data['date'])

        Market_Df = pd.DataFrame(columns=Market_Data['fields'])
        for data in Market_Data['data']:
            Market_Df_len = len(Market_Df)
            Market_Df.loc[Market_Df_len] = data
        
        print(Market_Df)

        return Market_Df
    else:
        return None