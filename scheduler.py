# -*- coding: utf-8 -*-
"""
股票盤後資訊自動化排程爬取
使用 schedule 套件進行排程
"""
import schedule
import time
from datetime import datetime
from logger import logger
from after_market import Get_All_Stock_After_Market_Info
from db import StockDB
import pandas as pd


class StockScheduler:
    """股票爬蟲排程器"""

    def __init__(self, stock_list=None):
        """
        初始化排程器
        Args:
            stock_list: 要爬取的股票代碼列表，預設為 ['2330', '2317']
        """
        if stock_list is None:
            # 預設爬取台積電、鴻海
            self.stock_list = ['2330', '2317']
        else:
            self.stock_list = stock_list

        self.db = StockDB()
        logger.info(f"排程器初始化完成，股票清單：{self.stock_list}")

    def crawl_and_save(self):
        """爬取並儲存股票盤後資訊"""
        logger.info("=" * 60)
        logger.info(f"開始執行排程任務 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        # 連接資料庫
        if not self.db.connect():
            logger.error("資料庫連接失敗，取消本次爬取")
            return

        success_count = 0
        fail_count = 0

        for stock_code in self.stock_list:
            try:
                logger.info(f"\n處理股票：{stock_code}")

                # 獲取盤後資訊
                info = Get_All_Stock_After_Market_Info(stock_code)

                # 儲存成交資訊到資料庫
                if info['trading_info'] is not None:
                    self.db.insert_stock_data(info['trading_info'], stock_code)

                # 儲存其他資訊到 CSV（可根據需求改為資料庫）
                self.save_to_csv(stock_code, info)

                success_count += 1
                logger.info(f"✓ {stock_code} 處理完成")

                # 避免請求過於頻繁
                time.sleep(5)

            except Exception as e:
                fail_count += 1
                logger.error(f"✗ {stock_code} 處理失敗：{e}")

        # 關閉資料庫連接
        self.db.disconnect()

        logger.info("=" * 60)
        logger.info(f"排程任務完成 - 成功：{success_count}，失敗：{fail_count}")
        logger.info("=" * 60)

    def save_to_csv(self, stock_code, info):
        """
        儲存盤後資訊到 CSV
        Args:
            stock_code: 股票代碼
            info: 盤後資訊字典
        """
        date = info['date']
        csv_dir = 'data'

        import os
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # 儲存三大法人資料
        if info['institutional_investors'] is not None:
            csv_file = os.path.join(csv_dir, f'{stock_code}_institutional_{date}.csv')
            info['institutional_investors'].to_csv(csv_file, index=False, encoding='utf-8-sig')
            logger.info(f"已儲存三大法人資料：{csv_file}")

        # 儲存融資融券資料
        if info['margin_trading'] is not None:
            csv_file = os.path.join(csv_dir, f'{stock_code}_margin_{date}.csv')
            info['margin_trading'].to_csv(csv_file, index=False, encoding='utf-8-sig')
            logger.info(f"已儲存融資融券資料：{csv_file}")

        # 儲存本益比資料
        if info['pe_ratio'] is not None:
            csv_file = os.path.join(csv_dir, f'{stock_code}_pe_{date}.csv')
            info['pe_ratio'].to_csv(csv_file, index=False, encoding='utf-8-sig')
            logger.info(f"已儲存本益比資料：{csv_file}")

    def setup_schedule(self, run_time="14:30"):
        """
        設定排程時間
        Args:
            run_time: 執行時間，格式為 "HH:MM"，預設為每日 14:30（盤後）
        """
        schedule.every().day.at(run_time).do(self.crawl_and_save)
        logger.info(f"已設定排程：每日 {run_time} 執行爬取任務")

    def run_once(self):
        """立即執行一次爬取任務"""
        logger.info("執行單次爬取任務")
        self.crawl_and_save()

    def run_forever(self):
        """持續運行排程器"""
        logger.info("排程器開始運行，按 Ctrl+C 停止")

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分鐘檢查一次
        except KeyboardInterrupt:
            logger.info("\n排程器已停止")


def load_stock_list_from_csv(csv_file='stock_name.csv'):
    """
    從 CSV 檔案載入股票清單
    Args:
        csv_file: CSV 檔案路徑
    Returns:
        股票代碼列表
    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        # 假設股票代碼在第二欄
        stock_codes = df.iloc[:, 1].astype(str).tolist()
        logger.info(f"從 {csv_file} 載入 {len(stock_codes)} 支股票")
        return stock_codes
    except Exception as e:
        logger.error(f"載入股票清單失敗：{e}")
        return ['2330', '2317']  # 預設值


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='股票盤後資訊爬取排程器')
    parser.add_argument('--mode', choices=['once', 'schedule'], default='once',
                        help='執行模式：once（立即執行一次）、schedule（排程執行）')
    parser.add_argument('--stocks', nargs='+', help='股票代碼列表，例如：2330 2317')
    parser.add_argument('--time', default='14:30', help='排程執行時間，格式：HH:MM')
    parser.add_argument('--csv', help='從 CSV 檔案載入股票清單')

    args = parser.parse_args()

    # 決定股票清單
    if args.csv:
        stock_list = load_stock_list_from_csv(args.csv)
    elif args.stocks:
        stock_list = args.stocks
    else:
        # 使用預設清單
        stock_list = ['2330', '2317', '2454', '2881', '2882']  # 台積電、鴻海、聯發科、富邦金、國泰金

    # 創建排程器
    scheduler = StockScheduler(stock_list)

    if args.mode == 'once':
        # 立即執行一次
        scheduler.run_once()
    else:
        # 設定排程並持續運行
        scheduler.setup_schedule(args.time)
        scheduler.run_forever()
