from often import *

def Get_Futures():
    
    Futures_Data_URL = f'https://www.wantgoo.com/stock/futures/_openinterestin30days?top=25'
    headers = {'User-Agent': 'Mozilla/5.0',
                'Cookie': 'BID=68712885-7B4D-4E7D-8308-21A4A96FA0F6; _hjid=3afd2b14-71f9-4e48-b59f-e01af5167951; _ga=GA1.2.1976740203.1624471427; _smt_uid=60d37782.1655ca1d; BrowserMode=Web; _gcl_au=1.1.1702182853.1624471428; hblid=7pMrcsEHIB9oPT3I3h7B70HloBb4jLar; olfsk=olfsk4293187356974473; wcsid=EyxiozdlSMgqhHZP3h7B70HOaL64jAob; _okdetect=%7B%22token%22%3A%2216256966004650%22%2C%22proto%22%3A%22https%3A%22%2C%22host%22%3A%22www.wantgoo.com%22%7D; _okbk=cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1625696600927%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C; _ok=8391-691-10-7433; idUserName=ericmeme321%40gmail.com; authorizedKey=BvW4wM%2btAFEkJXv%2fBEDFpQz%2bnbxMv8Up; UserName=BvW4wM%2btAFEkJXv%2fBEDFpQz%2bnbxMv8Up; NickName=ericmeme321; UserAccount=ericmeme321%40gmail.com; UnReadMailCount=0; Member_No=298398; IsLogin=True; urls=m.wantgoo.com; img=https%3a%2f%2fwww.wantgoo.com%2fimage%2fdisplaydefault1.png; Email=ericmeme321%40gmail.com; AdState=Show; MemberLevel=Normal; member_token=eyJpZCI6Mjk4Mzk4LCJ1c2VyTmFtZSI6ImVyaWNtZW1lMzIxQGdtYWlsLmNvbSIsIm5pY2tOYW1lIjoiZXJpY21lbWUzMjEiLCJoZWFkc2hvdCI6Imh0dHBzOi8vaW1nLndhbnRnb28uY29tL3dhbnRnb29maWxlcy91cGxvYWRmaWxlcy9kZWZhdWx0LW1lbWJlci1oZWFkc2hvdC5wbmcifQ..~70ba68b93dbbe6b3b374e0cc2dab7907c8ea73e931a2be6b7386d3d2de378396; _oklv=1625699386870%2CEyxiozdlSMgqhHZP3h7B70HOaL64jAob'}
    try:
        res = requests.get(Futures_Data_URL, headers=headers)
        soup = BeautifulSoup(res.text,"html.parser") #將網頁資料以html.parser
        table = soup.find(id="tab4")
        columns = ['日期', '外資多方口數', '外資空方口數', '小外資多方口數', '小外資空方口數', '自營多方口數', 
                '自營空方口數', '投信多方口數', '投信空方口數', '期貨(漲跌%)', '現貨(漲跌%)', '價差']
        
        trs = table.find_all('tr')[2:]        
        rows = list()
        for tr in trs:
            rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])

        Futures_Df = pd.DataFrame(data=rows, columns=columns)
        print(Futures_Df)

    except:
        print('Request URL error')

    return Futures_Df