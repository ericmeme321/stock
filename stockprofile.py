from often import *

def Get_Stock_Profile(Stock_Name):

    All_Stock_Profile_URL = f'https://www.wantgoo.com/stock/{Stock_Name}/company-profile-data'
    All_Stock_Profile = crawler(All_Stock_Profile_URL)


    columns = ['股票代號', '公司名稱', '成立日期', '董事長' ,'總經理' ,'實收資本額' ,'已發行普通股數'
            ,'發言人' ,'代理發言人' ,'總機電話' ,'傳真號碼' ,'統一編號' ,'公司網站' ,'公司地址' ,'電子郵件'
            ,'英文簡稱' ,'英文全名' ,'英文通訊地址' ,'主要經營業務' ,'實收資本額' ,'已發行普通股數' ,'特別股'
            ,'特別股發行' ,'公司債發行' ,'股票過戶機構' ,'股票過戶地址' ,'過戶機構電話' ,'簽證會計事務所'
            ,'變更前名稱' ,'簽證會計師  1' ,'變更前簡稱' ,'簽證會計師2' ,'變更核準日' ,'備註']
    i = 0
    dic = dict()
    for c in All_Stock_Profile:
        dic[columns[i]] = All_Stock_Profile[c]
        i+=1    
    
    for key, value in dic.items():
        print(key, ':', value)
    print()

    csv_file = 'C:/temp/' + str(Stock_Name) + str(dic['公司名稱']) + '.csv'
    try:
        with open(csv_file, 'w', encoding='utf-8-sig') as f:  
            writer = csv.writer(f)
            for k, v in dic.items():
                writer.writerow([k, v])
    except IOError:
        print("I/O error")

    return

if __name__ == '__main__':
    df = pd.read_csv("股票.csv")
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    Stock_Name_Df = df['有價證券代號及名稱']
    for i in Stock_Name_Df:
        if i[0:4].isdigit():
            try:
                Get_Stock_Profile(i[0:4])
                time.sleep(random.uniform(1, 5))
            except TypeError:
                print(i+'\n')
                continue