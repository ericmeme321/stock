#!/bin/bash
# 股票爬蟲系統套件安裝腳本

echo "======================================"
echo "  股票爬蟲系統 - 套件安裝"
echo "======================================"
echo ""

echo "正在安裝必要套件..."
pip install -r requirements.txt

echo ""
echo "======================================"
echo "  安裝完成！"
echo "======================================"
echo ""
echo "現在可以執行以下程式："
echo "  - python main.py           # 原有的主程式"
echo "  - python stock_crawler.py  # 新版整合主程式"
echo "  - python scheduler.py      # 自動化排程器"
echo ""
