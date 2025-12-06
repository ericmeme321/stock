# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import Error
from config import config


class StockDB:
    """股票資料庫操作類"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """連接資料庫"""
        try:
            self.connection = mysql.connector.connect(
                host=config.db_host,
                database=config.db_database,
                user=config.db_user,
                password=config.db_password,
                port=config.db_port
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                db_info = self.connection.get_server_info()
                print(f"[成功] 已連接到 MySQL 資料庫，版本：{db_info}")
                return True

        except Error as e:
            print(f"[錯誤] 資料庫連接失敗：{e}")
            return False

    def disconnect(self):
        """關閉資料庫連接"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("[資訊] 資料庫連線已關閉")

    def create_table_if_not_exists(self, table_name):
        """如果表格不存在則創建"""
        try:
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                uid INT AUTO_INCREMENT PRIMARY KEY,
                date VARCHAR(20) NOT NULL,
                open DECIMAL(10, 2),
                close DECIMAL(10, 2),
                high DECIMAL(10, 2),
                low DECIMAL(10, 2),
                vol BIGINT,
                rate VARCHAR(10),
                UNIQUE KEY unique_date (date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            self.cursor.execute(create_table_sql)
            print(f"[資訊] 確保表格 {table_name} 存在")
            return True

        except Error as e:
            print(f"[錯誤] 創建表格失敗：{e}")
            return False

    def insert_stock_data(self, stock_data, stock_code):
        """插入股票資料"""
        if stock_data is None or len(stock_data) == 0:
            print("[警告] 沒有資料可插入")
            return False

        table_name = f"tw_{stock_code}"

        try:
            # 創建表格
            self.create_table_if_not_exists(table_name)

            # 使用 REPLACE INTO 避免重複插入
            sql = f"""
            REPLACE INTO {table_name}
            (date, open, close, high, low, vol, rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            inserted_count = 0
            for i in range(len(stock_data)):
                row = stock_data.loc[i]
                new_data = (
                    str(row['日期']),
                    str(row['開盤價']),
                    str(row['收盤價']),
                    str(row['最高價']),
                    str(row['最低價']),
                    str(row['成交量']),
                    str(row['漲跌幅']) if '漲跌幅' in row else '0'
                )
                self.cursor.execute(sql, new_data)
                inserted_count += 1

            self.connection.commit()
            print(f"[成功] 已插入 {inserted_count} 筆資料到表格 {table_name}")
            return True

        except Error as e:
            print(f"[錯誤] 資料插入失敗：{e}")
            self.connection.rollback()
            return False

    def query_stock_data(self, stock_code, limit=30):
        """查詢股票資料"""
        table_name = f"tw_{stock_code}"
        try:
            sql = f"SELECT * FROM {table_name} ORDER BY date DESC LIMIT %s"
            self.cursor.execute(sql, (limit,))
            results = self.cursor.fetchall()
            return results

        except Error as e:
            print(f"[錯誤] 查詢資料失敗：{e}")
            return None


def DBinsert(stock_data, stock_name):
    """向下兼容的函數"""
    db = StockDB()
    if db.connect():
        result = db.insert_stock_data(stock_data, stock_name)
        db.disconnect()
        return result
    return False