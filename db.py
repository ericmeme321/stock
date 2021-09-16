import mysql.connector
from mysql.connector import Error


def DBinsert(stock_data, stock_name):
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='stock', # 資料庫名稱
            user='root',        # 帳號
            password='')  # 密碼

        if connection.is_connected():

            # 顯示資料庫版本
            # db_Info = connection.get_server_info()
            # print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            # cursor = connection.cursor()
            # cursor.execute("SELECT DATABASE();")
            # record = cursor.fetchone()
            # print("目前使用的資料庫：", record)
            stock_name = "tw_" + stock_name
            cursor = connection.cursor()
            if not stock_name in cursor:
                cursor.execute("CREATE TABLE " + stock_name + " (uid INT(5) AUTO_INCREMENT PRIMARY KEY\
                ,date VARCHAR(10), open FLOAT(10), close FLOAT(10), high FLOAT(10), low FLOAT(10), vol INT(10)\
                , rate VARCHAR(10));")
            sql = "INSERT INTO "+ stock_name +" (date, open, close, high, low, vol, rate) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            for i in range(len(stock_data)):
                row = stock_data.loc[i]
                new_data = (str(row['日期']), str(row['開盤價']), str(row['收盤價']), 
                    str(row['最高價']), str(row['最低價']), str(row['成交量']), str(row['漲跌幅']))
                cursor.execute(sql, new_data)
                # 確認資料有存入資料庫
                connection.commit()
            
            print("資料插入成功")

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    
    return