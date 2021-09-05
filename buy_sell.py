from often import *

def Get_Branch_Feature(Stock_Name, Agent_ID):
    Agent_ID_EX = ""
    flg = True
    for i in range(4):
        if Agent_ID[i].isalpha() and flg:
            Agent_ID_EX += '(' + Agent_ID[i] + ')'
            flg = False
        else:
            Agent_ID_EX += Agent_ID[i]

    Begin_Date = "2021/01/01"
    End_Date = "2021/07/14"
    Branch_Feature_URL  = f'https://www.wantgoo.com/stock/{Stock_Name}/major-investors/branch-buysell-agent-data/{Agent_ID_EX}?endDate={End_Date}&beginDate={Begin_Date}'
    Temp_Data = crawler(Branch_Feature_URL)
    Branch_Feature_Data = Temp_Data['data']
    
    idx = {'日期':[],
            '券商分點':[],
            '買張':[],
            '買價':[],
            '賣張':[],
            '賣價':[],
            '買賣超':[]}
 
    Branch_Feature_Data_Df = pd.DataFrame(idx)

    for c in Branch_Feature_Data:
        t = c.get('date')
        Agent_Name = c.get('agentName')
        Buy_Quantities = c.get('buyQuantities')
        Sell_Quantities = c.get('sellQuantities')
        Buy_Price_Average = c.get('buyPriceAvg')
        Sell_Price_Average = c.get('sellPriceAvg')
        if Buy_Quantities != None and Sell_Quantities != None:
            if Buy_Quantities - Sell_Quantities > 0:
                Buy_Or_Sell = '+'
            elif Buy_Quantities - Sell_Quantities < 0:
                Buy_Or_Sell = '-'
            else:
                Buy_Or_Sell = 'Same'
        else:
            Buy_Or_Sell = 'X'

        Branch_Feature_Data_List = []
        Branch_Feature_Data_List.extend([t, Agent_Name, Buy_Quantities, Buy_Price_Average, Sell_Quantities, Sell_Price_Average, Buy_Or_Sell])

        Branch_Feature_Data_Df_len = len(Branch_Feature_Data_Df)
        Branch_Feature_Data_Df.loc[Branch_Feature_Data_Df_len] = Branch_Feature_Data_List

    # Branch_Feature_Data_Df['買張'] = Branch_Feature_Data_Df['買張'].astype(int)
    # Branch_Feature_Data_Df['賣張'] = Branch_Feature_Data_Df['賣張'].astype(int)

    print(Branch_Feature_Data_Df)
    print()

    return Branch_Feature_Data_Df


def Get_Branch_Buy_Sell_Data(Stock_Name):
    
    # Begin_Date = input("開始時間(例:20210701) : ")
    # End_Date = input("結束時間(例:20210701) : ")
    Begin_Date = "2021/07/14"
    End_Date = "2021/07/14"
    Branch_Buy_Sell_Data_URL = f'https://www.wantgoo.com/stock/{Stock_Name}/major-investors/branch-buysell-data?isOverBuy=true&endDate={End_Date}&beginDate={Begin_Date}&v=298398'
    Temp_Data = crawler(Branch_Buy_Sell_Data_URL)
    Branch_Buy_Sell_Data = Temp_Data['data']


    idx = {'編號':[],
            '券商分點':[],
            '買價':[],
            '賣價':[],
            '均價':[],
            '買張':[],
            '賣張':[],}
    
    Branch_Buy_Sell_Data_Df = pd.DataFrame(idx)

    for c in Branch_Buy_Sell_Data:
        Agent_ID = c.get('agentId')
        Agent_Name = c.get('agentName')
        Buy_Quantities = c.get('buyQuantities')
        Sell_Quantities = c.get('sellQuantities')
        Buy_Price_Average = c.get('buyPriceAvg')
        Sell_Price_Average = c.get('sellPriceAvg')

        Price_Average = Calculate_Price_Average(Buy_Price_Average, Sell_Price_Average, Buy_Quantities, Sell_Quantities)
        Price_Average_List = [Price_Average]
        Price_Average_List = Display_Two_Decimal_Place(Price_Average_List)

        Branch_Buy_Sell_Data_List = []
        Branch_Buy_Sell_Data_List.extend([Agent_ID, Agent_Name, Buy_Price_Average, Sell_Price_Average, Price_Average_List[0]
                                            , Buy_Quantities, Sell_Quantities])


        Branch_Buy_Sell_Df_len = len(Branch_Buy_Sell_Data_Df)
        Branch_Buy_Sell_Data_Df.loc[Branch_Buy_Sell_Df_len] = Branch_Buy_Sell_Data_List

    Branch_Buy_Sell_Data_Df['買張'] = Branch_Buy_Sell_Data_Df['買張'].astype(int)
    Branch_Buy_Sell_Data_Df['賣張'] = Branch_Buy_Sell_Data_Df['賣張'].astype(int)

    print(Branch_Buy_Sell_Data_Df)
    print()

    for c in Branch_Buy_Sell_Data_Df['編號']:        
        Branch_Feature_Data_Df = Get_Branch_Feature(Stock_Name, c)

    return Branch_Buy_Sell_Data_Df

def Get_Specific_Brach_Buy_Sell_Data(Stock_Name, Agent_ID):
    Agent_ID = Agent_ID[:3] + '(' + Agent_ID[3:4] + ')'
    # Begin_Date = input("開始時間(例:20210701) : ")
    # End_Date = input("結束時間(例:20210701) : ")
    Begin_Date = "2021/06/07"
    End_Date = "2021/07/09"
    Specific_Branch_Buy_Sell_Data_URL = f'https://www.wantgoo.com/stock/{Stock_Name}/major-investors/branch-buysell-agent-data/{Agent_ID}?v=298398&endDate={End_Date}&beginDate={Begin_Date}'
    Temp_Data = crawler(Specific_Branch_Buy_Sell_Data_URL)
    Specific_Branch_Buy_Sell_Data = Temp_Data['data']

    idx = {'日期':[],
            '買價':[],
            '賣價':[],
            '均價':[],
            '買張':[],
            '賣張':[],}

    Specific_Branch_Buy_Sell_Data_Df = pd.DataFrame(idx)

    flg = True
    for c in Specific_Branch_Buy_Sell_Data:
        if flg:
            print()
            print(c['agentName'])
            flg = False

        Date = c['date']    
        Buy_Quantities = c['buyQuantities']
        Sell_Quantities = c['sellQuantities']
        Buy_Price_Average = c['buyPriceAvg']
        Sell_Price_Average = c['sellPriceAvg']

        Price_Average = Calculate_Price_Average(Buy_Price_Average, Sell_Price_Average, Buy_Quantities, Sell_Quantities)
        Price_Average_List = [Price_Average]
        Price_Average_List = Display_Two_Decimal_Place(Price_Average_List)

        Specific_Branch_Buy_Sell_Data_List = []
        Specific_Branch_Buy_Sell_Data_List.extend([Date, Buy_Price_Average, Sell_Price_Average, Price_Average_List[0]
                                            , Buy_Quantities, Sell_Quantities])


        Specific_Branch_Buy_Sell_Data_Df_len = len(Specific_Branch_Buy_Sell_Data_Df)
        Specific_Branch_Buy_Sell_Data_Df.loc[Specific_Branch_Buy_Sell_Data_Df_len] = Specific_Branch_Buy_Sell_Data_List

    print(Specific_Branch_Buy_Sell_Data_Df)
    print()

    return  Specific_Branch_Buy_Sell_Data_Df

def Get_Broker_Buy_Sell_Rank_Data(Agent_ID):
    Agent_ID = Agent_ID.upper()
    day = input("幾日前資料 : ")
    Broker_Buy_Sell_Rank_Data_URL = f'https://www.wantgoo.com/stock/major-investors/broker-buy-sell-rank-data?during={day}&majorId={Agent_ID}&orderBy=amount'
    Broker_Buy_Sell_Rank_Data = crawler(Broker_Buy_Sell_Rank_Data_URL)
    
    idx = {'股票代號':[],
            '股票名稱':[],
            '買張':[],
            '賣張':[],
            '均價':[],
            '總金額':[],}

    Broker_Buy_Sell_Rank_Data_Df = pd.DataFrame(idx)

    for c in Broker_Buy_Sell_Rank_Data:
        Stock_No = c['stockNo']
        Stock_Name = c['name']
        Buy_Quantities = c['buyQuantities']
        Sell_Quantities = c['sellQuantities']
        Price_Average = c['avgPrice']
        Amount = c['amount']

        Temp_List = [Price_Average, Amount]
        Temp_List = Display_Two_Decimal_Place(Temp_List)

        Broker_Buy_Sell_Rank_Data_List = []
        Broker_Buy_Sell_Rank_Data_List.extend([Stock_No, Stock_Name, Buy_Quantities, Sell_Quantities
                                                , Temp_List[0], Temp_List[1]])


        Broker_Buy_Sell_Rank_Data_Df_len = len(Broker_Buy_Sell_Rank_Data_Df)
        Broker_Buy_Sell_Rank_Data_Df.loc[Broker_Buy_Sell_Rank_Data_Df_len] = Broker_Buy_Sell_Rank_Data_List


    Broker_Buy_Sell_Rank_Data_Df['買張'] = Broker_Buy_Sell_Rank_Data_Df['買張'].astype(int)
    Broker_Buy_Sell_Rank_Data_Df['賣張'] = Broker_Buy_Sell_Rank_Data_Df['賣張'].astype(int)

    print(Broker_Buy_Sell_Rank_Data_Df)
    print()

    # Broker_Buy_Sell_Rank_Data_Df.to_csv('C:/temp/'+Agent_ID+'_'+datetime.today().strftime("%Y-%m-%d")+'.csv',encoding='utf_8_sig', header=True)

    return Broker_Buy_Sell_Rank_Data_Df