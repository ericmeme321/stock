# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from config import config


def setup_logger(name='stock_crawler'):
    """
    設定日誌系統
    Args:
        name: logger 名稱
    Returns:
        logger 實例
    """
    # 創建 logger
    logger = logging.getLogger(name)

    # 設定日誌級別
    log_level = getattr(logging, config.log_level, logging.INFO)
    logger.setLevel(log_level)

    # 避免重複添加 handler
    if logger.handlers:
        return logger

    # 創建日誌目錄
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 文件 handler - 記錄所有日誌
    log_file = os.path.join(log_dir, config.log_file)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 錯誤日誌 handler - 只記錄錯誤
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)

    # Console handler - 輸出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 設定日誌格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加 handlers
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger


# 創建全域 logger 實例
logger = setup_logger()
