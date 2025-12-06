# -*- coding: utf-8 -*-
"""
盤後資訊爬取模組
包含個股成交資訊、三大法人、融資融券等資料
"""
from often import *
from logger import logger


def Get_Stock_Trading_Info(stock_code, date=None):
    """
    獲取個股盤後成交資訊（單日）
    Args:
        stock_code: 股票代碼
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取 {stock_code} 的個股成交資訊，日期：{date}")

    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_code}'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        logger.info(f"成功取得 {stock_code} 共 {len(df)} 筆資料")
        return df
    else:
        logger.error(f"無法取得 {stock_code} 的成交資訊")
        return None


def Get_Institutional_Investors(date=None):
    """
    獲取三大法人買賣超統計（全市場）
    Args:
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取三大法人買賣超統計，日期：{date}")

    url = f'https://www.twse.com.tw/fund/BFI82U?response=json&dayDate={date}&type=day'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        logger.info(f"成功取得三大法人資料，共 {len(df)} 筆")
        return df
    else:
        logger.error("無法取得三大法人買賣超統計")
        return None


def Get_Stock_Institutional_Investors(stock_code, date=None):
    """
    獲取個股三大法人買賣超
    Args:
        stock_code: 股票代碼
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取 {stock_code} 的三大法人買賣超，日期：{date}")

    url = f'https://www.twse.com.tw/fund/T86?response=json&date={date}&selectType=ALL'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        # 篩選特定股票
        stock_df = df[df.iloc[:, 0] == stock_code]

        if len(stock_df) > 0:
            logger.info(f"成功取得 {stock_code} 的三大法人資料")
            return stock_df
        else:
            logger.warning(f"找不到 {stock_code} 的三大法人資料")
            return None
    else:
        logger.error(f"無法取得 {stock_code} 的三大法人資料")
        return None


def Get_Margin_Trading(date=None):
    """
    獲取融資融券餘額（全市場）
    Args:
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取融資融券餘額，日期：{date}")

    url = f'https://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date={date}&selectType=ALL'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        logger.info(f"成功取得融資融券資料，共 {len(df)} 筆")
        return df
    else:
        logger.error("無法取得融資融券餘額")
        return None


def Get_Stock_Margin_Trading(stock_code, date=None):
    """
    獲取個股融資融券餘額
    Args:
        stock_code: 股票代碼
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    df = Get_Margin_Trading(date)

    if df is not None and len(df) > 0:
        # 篩選特定股票（股票代碼在第一欄）
        stock_df = df[df.iloc[:, 0] == stock_code]

        if len(stock_df) > 0:
            logger.info(f"成功取得 {stock_code} 的融資融券資料")
            return stock_df
        else:
            logger.warning(f"找不到 {stock_code} 的融資融券資料")
            return None
    else:
        return None


def Get_Stock_PE_Ratio(date=None):
    """
    獲取個股本益比、殖利率、股價淨值比
    Args:
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取本益比、殖利率資料，日期：{date}")

    url = f'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date={date}&selectType=ALL'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        logger.info(f"成功取得本益比資料，共 {len(df)} 筆")
        return df
    else:
        logger.error("無法取得本益比資料")
        return None


def Get_Stock_PE_Ratio_By_Code(stock_code, date=None):
    """
    獲取特定個股的本益比、殖利率、股價淨值比
    Args:
        stock_code: 股票代碼
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    df = Get_Stock_PE_Ratio(date)

    if df is not None and len(df) > 0:
        # 篩選特定股票
        stock_df = df[df.iloc[:, 0] == stock_code]

        if len(stock_df) > 0:
            logger.info(f"成功取得 {stock_code} 的本益比資料")
            return stock_df
        else:
            logger.warning(f"找不到 {stock_code} 的本益比資料")
            return None
    else:
        return None


def Get_Day_Trading_Info(date=None):
    """
    獲取當日沖銷交易標的及成交量值
    Args:
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        DataFrame 或 None
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取當日沖銷交易資料，日期：{date}")

    url = f'https://www.twse.com.tw/exchangeReport/FMTQIK?response=json&date={date}'

    data = crawler(url)

    if data and data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])
        logger.info(f"成功取得當日沖銷交易資料，共 {len(df)} 筆")
        return df
    else:
        logger.error("無法取得當日沖銷交易資料")
        return None


def Get_All_Stock_After_Market_Info(stock_code, date=None):
    """
    獲取個股完整盤後資訊（整合所有資料）
    Args:
        stock_code: 股票代碼
        date: 查詢日期(YYYYMMDD)，預設為最近交易日
    Returns:
        dict 包含所有盤後資訊
    """
    if date is None:
        date = Get_Latest_Trading_Date()

    logger.info(f"開始爬取 {stock_code} 的完整盤後資訊，日期：{date}")

    result = {
        'stock_code': stock_code,
        'date': date,
        'trading_info': None,
        'institutional_investors': None,
        'margin_trading': None,
        'pe_ratio': None
    }

    # 爬取各項資料
    result['trading_info'] = Get_Stock_Trading_Info(stock_code, date)
    result['institutional_investors'] = Get_Stock_Institutional_Investors(stock_code, date)
    result['margin_trading'] = Get_Stock_Margin_Trading(stock_code, date)
    result['pe_ratio'] = Get_Stock_PE_Ratio_By_Code(stock_code, date)

    logger.info(f"完成 {stock_code} 盤後資訊爬取")

    return result


if __name__ == '__main__':
    # 測試用
    stock_code = '2330'  # 台積電
    print(f"\n===== 測試爬取 {stock_code} 盤後資訊 =====\n")

    # 獲取完整盤後資訊
    info = Get_All_Stock_After_Market_Info(stock_code)

    print("\n----- 成交資訊 -----")
    if info['trading_info'] is not None:
        print(info['trading_info'].head())

    print("\n----- 三大法人 -----")
    if info['institutional_investors'] is not None:
        print(info['institutional_investors'])

    print("\n----- 融資融券 -----")
    if info['margin_trading'] is not None:
        print(info['margin_trading'])

    print("\n----- 本益比資訊 -----")
    if info['pe_ratio'] is not None:
        print(info['pe_ratio'])
