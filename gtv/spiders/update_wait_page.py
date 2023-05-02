import urllib

import pymysql
import scrapy

from gtv.settings import *


class UpdateWaitPageSpider(scrapy.Spider):
    name = "update_wait_page"
    allowed_domains = ["www.xlsp.fun"]
    base_url = "https://www.xlsp.fun"
    start_urls = []

    def __init__(self):
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        try:
            select = "select * from t_categories"
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
            for row in rows:
                if row[5] is None or row[5] is '403':
                    self.start_urls.append('%s%s' % (self.base_url, row[3]))
            print("结束    %d" % len(self.start_urls))
        except Exception as e:
            print("获取视频分类错误: ", e)
        pass

    def parse(self, response: scrapy.http.HtmlResponse):
        _url = response.url
        if response.status != 200:
            self._update_categories(_url)
            return
        try:
            _strSize = response.xpath('//*[@id="app"]/div[2]/div[3]/nav/div/div[1]/p/span[2]/text()').get()
            _strTotal = response.xpath('//*[@id="app"]/div[2]/div[3]/nav/div/div[1]/p/span[3]/text()').get()
            self._insert_page(_url)
            if _strSize is None or _strTotal is None:
                print("不翻页：%s" % _url)
                return
            _size = int(_strSize)
            _total = int(_strTotal)
            _temp = 1
            _len = (_total / _size)
            if (_total % _size) != 0:
                _len += 1
            while _temp < _len:
                _temp += 1
                _page = "%s?page=%d" % (_url, _temp)
                self._insert_page(_page)
        except Exception as e:
            print('数据解析出错：' + response.url + "**********" + e)

    def _update_categories(self, url: str):
        _sql = 'update `t_categories` set `status` = %d where `href` = "%s"' % (403, url)
        try:
            self.cursor.execute(_sql)
            self.db.commit()
        except pymysql.MySQLError as _:
            print("更新分类状态错误")

    def _insert_page(self, url: str):
        try:
            _select = 'select `id` from `t_pages`where `url` = "%s"' % url
            self.cursor.execute(_select)
            one = self.cursor.fetchone()
            self.db.commit()
            if one is None:
                try:
                    _insert = 'insert into `t_pages` (`url`) values ("%s")' % url
                    self.cursor.execute(_insert)
                    self.db.commit()
                except pymysql.MySQLError as _:
                    print("插入数据页错误")
        except pymysql.MySQLError as _:
            print("查询数据页错误")


