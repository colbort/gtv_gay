# -*- coding: utf-8 -*-
import pymysql
import scrapy

from gtv.items import GtvVideoItem
from gtv.settings import *
from gtv.spiders.common import parse_detail


class SpiderWaitSpider(scrapy.Spider):
    name = "spider_wait"
    allowed_domains = ["www.xlsp.fun"]
    base_url = "https://www.xlsp.fun"
    start_urls = []
    items = {}

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
            _select = 'select `href`, `image`, `title`, `date` from `t_videos_wait_spider`'
            self.cursor.execute(_select)
            rows = self.cursor.fetchall()
            for row in rows:
                _item = GtvVideoItem()
                _item["href"] = row[0]
                _item["image"] = row[1]
                _item["title"] = row[2]
                _item["date"] = row[3]
                self.items[row[0]] = _item
                _url = self.base_url + row[0]
                self.start_urls.append(_url)
        except Exception as e:
            print(e)
        pass

    def parse(self, response):
        if response.status != 200:
            print("请求失败：", response.status)
            return
        _href = response.url.replace(self.base_url, "")
        _item = self.items[_href]
        if _item is None:
            return
        item = parse_detail(response, _item, self.cursor, self.base_url, self.parse, self._get_video_detail,
                            self._create_spider)
        yield item

    @staticmethod
    def _get_video_detail(_, __):
        return False

    @staticmethod
    def _create_spider(_, __, ___, ____):
        pass
