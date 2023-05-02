# -*- coding: utf-8 -*-
import json
from time import sleep

import pymysql
import scrapy

from gtv.items import GtvVideoItem
from gtv.settings import *
from gtv.spiders.common import parse_detail


class SpiderWaitSpider(scrapy.Spider):
    name = "spider_recommend"
    allowed_domains = ["www.xlsp.fun"]
    base_url = "https://www.xlsp.fun"
    start_urls = []
    items = {}
    page = 0
    size = 1000
    sql = 'select `recommend` from `t_videos_detail` where `wait` is null limit %d, %d'

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
        self._get_data()

    def parse(self, response):
        if response.status != 200:
            print("请求失败：%d  %s" % (response.status, response.url))
            return
        _href = response.url.replace(self.base_url, "")
        _item = self.items[_href]
        if len(self.items) < 20:
            sleep(2)
            self.page = self.page + 1
            self._get_data()
            print('获取新数据 %d' % len(self.items))
            sleep(2)
        if _item is None:
            return
        item = parse_detail(response, _item, self.cursor, self.base_url, self.parse, self._get_video_detail,
                            self._create_spider)
        self._update_status(_href)
        yield item

    def _update_status(self, href: str):
        _update = "update `t_videos_detail` set `wait` = %d where `href` = '%s'" % (1, href)
        try:
            self.cursor.execute(_update)
            self.db.commit()
        except Exception as e:
            print("更新未爬取视频状态错误: ", e)
        pass

    def _get_data(self):
        _select = self.sql % (self.page, self.size)
        try:
            self.cursor.execute(_select)
            rows = self.cursor.fetchall()
            for row in rows:
                _jsons = json.loads(row[0])
                for _j in _jsons:
                    _item = GtvVideoItem()
                    _item["href"] = _j["href"]
                    _item["image"] = _j["image"]
                    _item["title"] = _j["title"]
                    _item["date"] = _j["date"]
                    self.items[_item["href"]] = _item
                    _url = self.base_url + _item["href"]
                    self.start_urls.append(_url)
        except Exception as e:
            print("获取未爬取视频错误: ", e)

    @staticmethod
    def _get_video_detail(_, __):
        return False

    @staticmethod
    def _create_spider(_, __, ___, ____):
        pass
