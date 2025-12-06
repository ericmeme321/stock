# -*- coding: utf-8 -*-
import configparser
import os

class Config:
    """配置管理類"""

    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file

        # 確保配置文件存在
        if os.path.exists(config_file):
            self.config.read(config_file, encoding='utf-8')
        else:
            print(f'[警告] 配置文件 {config_file} 不存在，使用預設值')

    # 資料庫配置
    @property
    def db_host(self):
        return self.config.get('DATABASE', 'host', fallback='localhost')

    @property
    def db_database(self):
        return self.config.get('DATABASE', 'database', fallback='stock')

    @property
    def db_user(self):
        return self.config.get('DATABASE', 'user', fallback='root')

    @property
    def db_password(self):
        return self.config.get('DATABASE', 'password', fallback='')

    @property
    def db_port(self):
        return self.config.getint('DATABASE', 'port', fallback=3306)

    # 爬蟲配置
    @property
    def crawler_max_retries(self):
        return self.config.getint('CRAWLER', 'max_retries', fallback=3)

    @property
    def crawler_timeout(self):
        return self.config.getint('CRAWLER', 'timeout', fallback=10)

    @property
    def crawler_sleep_min(self):
        return self.config.getint('CRAWLER', 'sleep_min', fallback=3)

    @property
    def crawler_sleep_max(self):
        return self.config.getint('CRAWLER', 'sleep_max', fallback=5)

    # 日誌配置
    @property
    def log_file(self):
        return self.config.get('LOGGING', 'log_file', fallback='stock_crawler.log')

    @property
    def log_level(self):
        return self.config.get('LOGGING', 'log_level', fallback='INFO')

    # 排程配置
    @property
    def after_market_time(self):
        return self.config.get('SCHEDULE', 'after_market_time', fallback='14:30')

# 創建全域配置實例
config = Config()
