import os
import sys

import pymysql

from gtv.items import HalfItem
from gtv.settings import *
from scrapy.cmdline import execute


class ReadCategories(object):
    def __init__(self):
        self.db = None
        self.cursor = None

        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        self._load_categories()

    def _load_categories(self):
        _select = 'select `id`, `href` from `t_videos`'
        self.cursor.execute(_select)
        rows = self.cursor.fetchall()
        for row in rows:
            _update = 'update `t_videos_detail` set `href` = "%s" where `id` = %d' % (row[1], row[0])
            print(_update)
            self.cursor.execute(_update)
            self.db.commit()


class UpdateCVTable(object):
    def __init__(self):
        self.db = None
        self.cursor = None

        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        self._load_categories()

    def _load_categories(self):
        _select = 'select `id`, `href` from `t_videos`'
        self.cursor.execute(_select)
        rows = self.cursor.fetchall()
        for row in rows:
            _update = 'update `t_index_c_v` set `href` = "%s" where `vid` = %d' % (row[1], row[0])
            print(_update)
            self.cursor.execute(_update)
            self.db.commit()


if __name__ == "__main__":
    # ReadCategories()
    # UpdateCVTable()
    # 添加当前项目的绝对地址
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # 执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
    # execute(['scrapy', 'crawl', 'update_wait_page'])
    # execute(['scrapy', 'crawl', 'videos'])
    execute(['scrapy', 'crawl', 'spider_wait'])
