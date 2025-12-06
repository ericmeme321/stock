# -*- coding: utf-8 -*-
"""
股票盤後資訊爬取系統 - 主程式
整合所有功能的統一入口
"""
import sys
from logger import logger
from after_market import *
from db import StockDB


def show_menu():
    """顯示主選單"""
    print("\n" + "=" * 60)
    print("     股票盤後資訊爬取系統 v2.0")
    print("=" * 60)
    print("1. 查詢個股成交資訊")
    print("2. 查詢三大法人買賣超（全市場）")
    print("3. 查詢個股三大法人買賣超")
    print("4. 查詢融資融券餘額（全市場）")
    print("5. 查詢個股融資融券餘額")
    print("6. 查詢本益比、殖利率（全市場）")
    print("7. 查詢個股本益比、殖利率")
    print("8. 查詢個股完整盤後資訊")
    print("9. 查詢加權指數資料")
    print("0. 離開系統")
    print("=" * 60)


def query_stock_trading():
    """查詢個股成交資訊"""
    stock_code = input("請輸入股票代碼：").strip()
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Stock_Trading_Info(stock_code, date)

    if df is not None:
        print("\n===== 個股成交資訊 =====")
        print(df)

        # 詢問是否儲存到資料庫
        save = input("\n是否儲存到資料庫？(y/n)：").strip().lower()
        if save == 'y':
            db = StockDB()
            if db.connect():
                db.insert_stock_data(df, stock_code)
                db.disconnect()


def query_institutional_investors():
    """查詢三大法人買賣超（全市場）"""
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Institutional_Investors(date)

    if df is not None:
        print("\n===== 三大法人買賣超統計 =====")
        print(df)


def query_stock_institutional():
    """查詢個股三大法人買賣超"""
    stock_code = input("請輸入股票代碼：").strip()
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Stock_Institutional_Investors(stock_code, date)

    if df is not None:
        print(f"\n===== {stock_code} 三大法人買賣超 =====")
        print(df)


def query_margin_trading():
    """查詢融資融券餘額（全市場）"""
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Margin_Trading(date)

    if df is not None:
        print("\n===== 融資融券餘額 =====")
        print(df.head(20))  # 只顯示前 20 筆


def query_stock_margin():
    """查詢個股融資融券餘額"""
    stock_code = input("請輸入股票代碼：").strip()
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Stock_Margin_Trading(stock_code, date)

    if df is not None:
        print(f"\n===== {stock_code} 融資融券餘額 =====")
        print(df)


def query_pe_ratio():
    """查詢本益比、殖利率（全市場）"""
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Stock_PE_Ratio(date)

    if df is not None:
        print("\n===== 本益比、殖利率資訊 =====")
        print(df.head(20))  # 只顯示前 20 筆


def query_stock_pe():
    """查詢個股本益比、殖利率"""
    stock_code = input("請輸入股票代碼：").strip()
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    df = Get_Stock_PE_Ratio_By_Code(stock_code, date)

    if df is not None:
        print(f"\n===== {stock_code} 本益比、殖利率 =====")
        print(df)


def query_all_after_market():
    """查詢個股完整盤後資訊"""
    stock_code = input("請輸入股票代碼：").strip()
    date_input = input("請輸入日期（YYYYMMDD，直接按 Enter 使用最近交易日）：").strip()

    date = date_input if date_input else None
    info = Get_All_Stock_After_Market_Info(stock_code, date)

    print(f"\n===== {stock_code} 完整盤後資訊 =====")

    if info['trading_info'] is not None:
        print("\n【成交資訊】")
        print(info['trading_info'].tail(5))  # 顯示最近 5 天

    if info['institutional_investors'] is not None:
        print("\n【三大法人】")
        print(info['institutional_investors'])

    if info['margin_trading'] is not None:
        print("\n【融資融券】")
        print(info['margin_trading'])

    if info['pe_ratio'] is not None:
        print("\n【本益比資訊】")
        print(info['pe_ratio'])

    # 詢問是否儲存
    save = input("\n是否儲存成交資訊到資料庫？(y/n)：").strip().lower()
    if save == 'y' and info['trading_info'] is not None:
        db = StockDB()
        if db.connect():
            db.insert_stock_data(info['trading_info'], stock_code)
            db.disconnect()


def query_market_data():
    """查詢加權指數資料"""
    from market2 import Get_Market_Data

    df = Get_Market_Data()
    if df is not None:
        print("\n===== 加權指數資料 =====")
        print(df)


def main():
    """主程式"""
    logger.info("股票爬蟲系統啟動")

    while True:
        try:
            show_menu()
            choice = input("\n請選擇功能（輸入數字）：").strip()

            if choice == '1':
                query_stock_trading()
            elif choice == '2':
                query_institutional_investors()
            elif choice == '3':
                query_stock_institutional()
            elif choice == '4':
                query_margin_trading()
            elif choice == '5':
                query_stock_margin()
            elif choice == '6':
                query_pe_ratio()
            elif choice == '7':
                query_stock_pe()
            elif choice == '8':
                query_all_after_market()
            elif choice == '9':
                query_market_data()
            elif choice == '0':
                print("\n感謝使用，再見！")
                logger.info("股票爬蟲系統正常結束")
                sys.exit(0)
            else:
                print("\n[錯誤] 無效的選項，請重新輸入")

            input("\n按 Enter 繼續...")

        except KeyboardInterrupt:
            print("\n\n程式已中斷")
            logger.info("股票爬蟲系統被使用者中斷")
            sys.exit(0)
        except Exception as e:
            logger.error(f"發生錯誤：{e}")
            print(f"\n[錯誤] {e}")
            input("\n按 Enter 繼續...")


if __name__ == '__main__':
    main()
