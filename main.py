from market import *
from stock import *
from buy_sell import *
from cash import *
from futures import *

# # get data
# import pandas_datareader as pdr

# # visual
# import matplotlib.pyplot as plt
# import mpl_finance as mpf
# import seaborn as sns

# #talib
# import talib


pd.set_option('display.unicode.ambiguous_as_wide',True)
pd.set_option('display.unicode.east_asian_width',True)

# def Show_Cadlestick_Chart(Stock_Df):
#     fig = plt.figure(figsize=(16, 8))
    
#     s = Stock_Df[['開盤價', '收盤價', '最高價', '最低價']]
#     s2 = Stock_Df[['開盤價', '收盤價', '成交量']]
#     s.columns = ['open', 'close', 'high', 'low']
#     s2.columns = ['open', 'close', 'volume']

    
#     s = s[::-1].reset_index(drop=True)
#     s = s.astype('f8')
#     s2 = s2[::-1].reset_index(drop=True)
#     s2 = s2.astype('f8')
#     sma_10 = talib.SMA(np.array(s['close']), 10)
#     sma_30 = talib.SMA(np.array(s['close']), 30)
#     s = s.reset_index().values
#     mf = s2['volume'].values
#     close = s2['close'].values.copy()
#     open = s2['open'].values.copy()
#     close[mf>0] = 1; open[mf>0] = 0
#     close[mf<=0] = 0; open[mf<=0] = 1
#     # 之後試fplt

#     ax = fig.add_axes([0.05,0.3,0.9,0.4])
#     ax2 = fig.add_axes([0.05,0.2,0.9,0.1])
#     # ax.set_xticks(range(0, len(Stock_Df['日期']), 10))
#     # ax.set_xticklabels(Stock_Df['日期'][::-10])

#     mpf.candlestick_ochl(ax, s, width=0.6, colorup='r', colordown='g', alpha=0.75)

#     plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] 
#     ax.plot(sma_10, label='10日均線')
#     ax.plot(sma_30, label='30日均線')

#     mpf.volume_overlay(ax2, s2['open'], s2['close'], s2['volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)
#     ax2.set_xticks(range(0, len(Stock_Df['日期']), 10))
#     ax2.set_xticklabels(Stock_Df['日期'][::-10])
    
#     ax.legend()
#     plt.show()
#     return

if __name__ == '__main__':
    ins = input("(1)加權指數資料查詢\n(2)股票資料查詢\n(3)股票券商分點資料查詢\n\
(4)股票特定券商分點資料查詢\n(5)特定券商分點資料查詢\n(6)資金流向查詢\n(7)三大法人期貨多空\n\
(8)pdf測試\n")

    if ins == '1':
        Market_Data = Get_Market_Data()
        Market_Minute_Data = Get_Market_Minute_Data()
    elif ins == '2':
        Stock_Name = input('股票代號 : ')
        Stock_Data = Get_Stock_Data(Stock_Name)
        # Stock_Minute_Date = Get_Stock_Minute_Data(Stock_Name)
    elif ins == '3':
        Stock_Name = input('股票代號 : ')
        Branch_Buy_Sell_Data = Get_Branch_Buy_Sell_Data(Stock_Name)
    elif ins == '4':
        Stock_Name = input('股票代號 : ')
        Agent_ID = input('券商編號 : ')
        Specific_Branch_Buy_Sell_Data = Get_Specific_Brach_Buy_Sell_Data(Stock_Name, Agent_ID)
    elif ins == '5':
        Agent_ID = input('券商編號 : ')
        Broker_Buy_Sell_Rank_Data = Get_Broker_Buy_Sell_Rank_Data(Agent_ID)
    elif ins == '6':
        Cash_Flow_Data = Get_Cash_Flow()
    elif ins == '7':
        Futures_Date = Get_Futures()
    elif ins == '8':
        Stock_Name = input('股票代號 : ')
        Get_Stock_information(Stock_Name)
