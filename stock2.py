from often import *
from requests_html import HTMLSession

def Get_TWStock_Data(Stock_Name):
    Now_Time = Get_Now()
    # num = input('資料筆數 : ')

    Stock_Data_URL = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210915&stockNo={Stock_Name}&_={Now_Time}'


    Stock_Data = crawler(Stock_Data_URL)


    if Stock_Data['stat'] == 'OK':
        print(Stock_Data['title'], Stock_Data['date'])

        Stock_Df = pd.DataFrame(columns=Stock_Data['fields'])
        for data in Stock_Data['data']:
            Stock_Df_len = len(Stock_Df)
            Stock_Df.loc[Stock_Df_len] = data
        
        print(Stock_Df)

        return Stock_Df
    else:
        return None

def Get_Stock_LegalPerson(Stock_Name):
    industry = Get_Stock_industry(Stock_Name)
    Now_Time = Get_Now()

    Stock_LegalPerson_URL = f'https://www.twse.com.tw/fund/T86?response=json&date=&selectType={industry}&_={Now_Time}'

    Stock_LegalPerson_Data = crawler(Stock_LegalPerson_URL)


    if Stock_LegalPerson_Data['stat'] == 'OK':
        print(Stock_LegalPerson_Data['title'], Stock_LegalPerson_Data['date'])

        Stock_LegalPerson_Df = pd.DataFrame(columns=Stock_LegalPerson_Data['fields'])
        for data in Stock_LegalPerson_Data['data']:
            if data[0] == Stock_Name:
                Stock_LegalPerson_Df_len = len(Stock_LegalPerson_Df)
                Stock_LegalPerson_Df.loc[Stock_LegalPerson_Df_len] = data
                break
        
        print(Stock_LegalPerson_Df)

        return Stock_LegalPerson_Df
    else:
        return None

def Get_Stock_industry(Stock_Name):
    Stock_Industry_URL = f'https://isin.twse.com.tw/isin/single_main.jsp?owncode={Stock_Name}&stockname='

    response = requests.get(Stock_Industry_URL) # 用 requests 的 get 方法把網頁抓下來
    soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
    data = soup.find_all('tr')[1].find_all_next('td')[6]
    industry = data.string

    dic =  {'水泥工業': '01', 
            '食品工業': '02',
            '塑膠工業': '03',
            '紡織纖維': '04',
            '電機機械': '05',
            '電器電纜': '06',
            '化學生技醫療': '07',
            '玻璃陶瓷': '08',
            '造紙工業': '09',
            '鋼鐵工業': '10',
            '橡膠工業': '11',
            '汽車工業': '12',
            '電子工業': '13',
            '建材營造': '14',
            '航運業': '15',
            '觀光事業': '16',
            '金融保險': '17',
            '貿易百貨': '18',
            '其他': '20',
            '化學工業': '21',
            '生技醫療業': '22',
            '油電燃氣業': '23',
            '半導體業': '24',
            '電腦及週邊設備業': '25',
            '光電業': '26',
            '通信網路業': '27',
            '電子零組件業': '28',
            '電子通路業': '29',
            '資訊服務業': '30',
            '其他電子業': '31'}
        
    return dic[industry]