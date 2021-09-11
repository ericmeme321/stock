from often import *

stock_name_list = pd.read_csv('stocklist.csv')
data = stock_name_list['有價證券代號及名稱 ']
for i in range(len(data)):
    data.iloc[i] = data.iloc[i][:4]
    
data.to_csv('stack_name.csv',encoding='utf_8_sig', header=True)