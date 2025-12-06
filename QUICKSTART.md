# 快速入門指南

## ❗ 遇到「什麼都沒顯示」的問題？

如果執行 `python main.py` 沒有任何顯示，這是因為**缺少必要的 Python 套件**。

## 🔧 解決方法

### 方法一：自動安裝（推薦）

```bash
# Linux/Mac
./install.sh

# Windows
pip install -r requirements.txt
```

### 方法二：手動安裝

```bash
pip install pandas numpy requests requests-html beautifulsoup4 lxml lxml_html_clean mysql-connector-python schedule
```

## ✅ 驗證安裝

安裝完成後，執行測試腳本：

```bash
python test_crawler.py
```

如果看到以下訊息表示安裝成功：

```
✓ 最近交易日：20251205
✓ 日誌系統正常
✓ 資料庫主機：localhost
```

## 🚀 開始使用

### 1. 原有程式（main.py）

```bash
python main.py
```

會顯示選單：
```
(1)加權指數資料查詢
(2)股票資料查詢
(3)資金流向查詢
(4)三大法人期貨多空
(5)股票三大法人資料查詢
```

### 2. 新版整合程式（推薦）

```bash
python stock_crawler.py
```

提供更多功能和更好的介面。

### 3. 自動化排程

```bash
# 立即爬取台積電和鴻海
python scheduler.py --mode once --stocks 2330 2317

# 每日 14:30 自動執行
python scheduler.py --mode schedule --time 14:30 --stocks 2330 2317
```

## 📋 常見問題

### Q1: 執行時出現 `ModuleNotFoundError`？

**原因**：缺少某個 Python 套件

**解決**：執行 `pip install -r requirements.txt`

### Q2: 出現資料庫連接錯誤？

**原因**：尚未設定資料庫或資料庫未啟動

**解決**：
1. 如果不需要儲存到資料庫，可以直接查看輸出結果
2. 如果需要資料庫功能：
   - 安裝 MySQL
   - 複製 `config.ini.example` 為 `config.ini`
   - 修改資料庫設定

### Q3: 爬取時出現錯誤？

**可能原因**：
- 非交易日（週末或假日）
- 網路連線問題
- 證交所網站維護

**解決**：
- 檢查日誌檔案：`logs/error.log`
- 確認網路連線正常
- 在交易日執行

## 💡 小提示

1. **首次使用**：建議先執行 `python test_crawler.py` 確認環境正常
2. **測試爬取**：使用台積電(2330)測試，因為資料最完整
3. **查看日誌**：所有執行記錄都在 `logs/` 目錄
4. **CSV 匯出**：爬取的資料會自動儲存到 `data/` 目錄

## 📞 需要幫助？

查看完整文檔：`README.md`
