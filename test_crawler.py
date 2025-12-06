# -*- coding: utf-8 -*-
"""
簡單測試腳本
用於驗證爬蟲功能是否正常
"""
from often import Get_Latest_Trading_Date
from logger import logger

print("=" * 60)
print("股票爬蟲系統測試")
print("=" * 60)

# 測試 1: 獲取最近交易日
print("\n[測試 1] 獲取最近交易日")
try:
    latest_date = Get_Latest_Trading_Date()
    print(f"✓ 最近交易日：{latest_date}")
except Exception as e:
    print(f"✗ 失敗：{e}")

# 測試 2: 測試 logger
print("\n[測試 2] 測試日誌系統")
try:
    logger.info("這是一條測試日誌")
    print("✓ 日誌系統正常，請查看 logs/stock_crawler.log")
except Exception as e:
    print(f"✗ 失敗：{e}")

# 測試 3: 測試配置讀取
print("\n[測試 3] 測試配置讀取")
try:
    from config import config
    print(f"✓ 資料庫主機：{config.db_host}")
    print(f"✓ 資料庫名稱：{config.db_database}")
    print(f"✓ 爬蟲重試次數：{config.crawler_max_retries}")
except Exception as e:
    print(f"✗ 失敗：{e}")

# 測試 4: 測試爬蟲功能（簡單測試）
print("\n[測試 4] 測試爬蟲功能（爬取台積電資料）")
print("注意：這個測試會實際連線到證交所網站")
test_crawl = input("是否進行爬蟲測試？(y/n)：").strip().lower()

if test_crawl == 'y':
    try:
        from after_market import Get_Stock_Trading_Info
        df = Get_Stock_Trading_Info('2330')
        if df is not None and len(df) > 0:
            print(f"✓ 成功爬取台積電資料，共 {len(df)} 筆")
            print("\n最近 3 筆資料：")
            print(df.head(3))
        else:
            print("✗ 無法取得資料（可能是非交易日或網路問題）")
    except Exception as e:
        print(f"✗ 失敗：{e}")
        import traceback
        traceback.print_exc()
else:
    print("⊘ 跳過爬蟲測試")

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)
