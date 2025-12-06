# 台股盤後資訊爬取系統 v2.0

一個完整的台股盤後資訊爬取系統，支援個股成交資訊、三大法人買賣超、融資融券、本益比等資料爬取，並提供自動化排程功能。

## 功能特色

- ✅ **個股日成交資訊**：爬取個股每日交易資料
- ✅ **三大法人買賣超**：追蹤法人動向
- ✅ **融資融券餘額**：了解市場籌碼
- ✅ **本益比、殖利率**：基本面分析指標
- ✅ **自動化排程**：每日定時自動爬取
- ✅ **資料庫儲存**：MySQL 資料持久化
- ✅ **日誌系統**：完整的執行記錄
- ✅ **錯誤處理**：重試機制與異常處理

## 系統架構

```
stock/
├── config.ini              # 配置檔案
├── config.py               # 配置管理模組
├── logger.py               # 日誌系統
├── often.py                # 通用工具函數
├── db.py                   # 資料庫操作
├── stock2.py               # 個股資料爬取
├── market2.py              # 市場資料爬取
├── after_market.py         # 盤後資訊爬取（新）
├── scheduler.py            # 自動化排程器（新）
├── stock_crawler.py        # 整合主程式（新）
├── requirements.txt        # 套件需求
└── logs/                   # 日誌目錄
    ├── stock_crawler.log
    └── error.log
```

## 安裝步驟

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

### 2. 設定資料庫

編輯 `config.ini` 檔案，設定資料庫連線資訊：

```ini
[DATABASE]
host = localhost
database = stock
user = root
password = your_password
port = 3306
```

### 3. 創建資料庫

```sql
CREATE DATABASE stock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 使用方式

### 方式一：互動式選單

執行主程式，透過選單操作：

```bash
python stock_crawler.py
```

功能選單：
1. 查詢個股成交資訊
2. 查詢三大法人買賣超（全市場）
3. 查詢個股三大法人買賣超
4. 查詢融資融券餘額（全市場）
5. 查詢個股融資融券餘額
6. 查詢本益比、殖利率（全市場）
7. 查詢個股本益比、殖利率
8. 查詢個股完整盤後資訊
9. 查詢加權指數資料

### 方式二：自動化排程

#### 立即執行一次（測試用）

```bash
python scheduler.py --mode once --stocks 2330 2317
```

#### 設定排程（每日自動執行）

```bash
python scheduler.py --mode schedule --time 14:30 --stocks 2330 2317 2454
```

#### 使用 CSV 股票清單

```bash
python scheduler.py --mode schedule --csv stock_name.csv
```

### 方式三：Python 模組引用

```python
from after_market import Get_All_Stock_After_Market_Info
from db import StockDB

# 爬取台積電盤後資訊
info = Get_All_Stock_After_Market_Info('2330')

# 儲存到資料庫
db = StockDB()
if db.connect():
    db.insert_stock_data(info['trading_info'], '2330')
    db.disconnect()
```

## 排程設定（Linux/Mac）

使用 crontab 設定每日自動執行：

```bash
# 編輯 crontab
crontab -e

# 新增以下內容（每日 14:30 執行）
30 14 * * 1-5 cd /path/to/stock && python scheduler.py --mode once --csv stock_name.csv
```

## 配置說明

### config.ini 配置項目

```ini
[DATABASE]
host = localhost          # 資料庫主機
database = stock         # 資料庫名稱
user = root              # 使用者名稱
password =               # 密碼
port = 3306              # 埠號

[CRAWLER]
max_retries = 3          # 最大重試次數
timeout = 10             # 連線逾時（秒）
sleep_min = 3            # 最小等待時間（秒）
sleep_max = 5            # 最大等待時間（秒）

[LOGGING]
log_file = stock_crawler.log  # 日誌檔案
log_level = INFO              # 日誌級別

[SCHEDULE]
after_market_time = 14:30     # 盤後執行時間
```

## 資料來源

所有資料來自台灣證券交易所公開資訊：
- 個股日成交資訊：https://www.twse.com.tw/
- 三大法人買賣超：https://www.twse.com.tw/
- 融資融券餘額：https://www.twse.com.tw/
- 本益比殖利率：https://www.twse.com.tw/

## 注意事項

1. **爬蟲禮儀**：請勿過於頻繁爬取，已內建 3-5 秒隨機延遲
2. **交易日限制**：僅交易日有資料，週末及國定假日無資料
3. **資料時間**：盤後資訊通常在下午 1:30 後更新
4. **資料庫權限**：確保 MySQL 使用者有建表和寫入權限

## 常見問題

### Q1: 無法連接資料庫？
A: 檢查 config.ini 中的資料庫設定是否正確，確認 MySQL 服務已啟動。

### Q2: 爬取失敗？
A: 查看 logs/error.log 了解錯誤原因，可能是網路問題或證交所 API 變更。

### Q3: 如何新增更多股票？
A: 編輯 stock_name.csv 或在執行時使用 --stocks 參數指定。

## 更新日誌

### v2.0 (2025-12-06)
- ✨ 新增完整盤後資訊爬取功能
- ✨ 新增自動化排程系統
- ✨ 新增日誌記錄功能
- ✨ 改進錯誤處理和重試機制
- ✨ 優化資料庫操作
- ✨ 新增配置檔案管理
- 🐛 修正硬編碼日期問題
- 🐛 改進 crawler 函數穩定性

### v1.0
- 基本爬蟲功能

## 授權

本專案僅供個人學習與研究使用。

## 作者

Stock Crawler Team
