# -*- coding: utf-8 -*-
import urllib

import pymysql
import scrapy
from lxml import etree

from gtv.items import GtvVideoItem
from gtv.settings import *
from gtv.spiders.common import parse_item, parse_detail


def _get_video_detail(cursor, href):
    try:
        select = "select * from t_videos where href=%s"
        cursor.execute(select, href)
        row = cursor.fetchone()
        if row is not None:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


class GtvVideosSpider(scrapy.Spider):
    name = 'videos'
    allowed_domains = ['danlanshipin.gay/old_gtv']
    base_url = "https://www.xlsp.fun"
    # start_urls = ['https://www.xlsp.fun/gtv/cate/%E5%85%B5%E5%93%A5%E5%93%A5']
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
            select = "select * from t_pages where `status` != 200"
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
            for row in rows:
                self.start_urls.append(row[1])
        except Exception as e:
            print("获取视频分类错误: ", e)
        pass

    def parse(self, response: scrapy.http.HtmlResponse):
        self._update_page_status(response.url, response.status)
        if response.status != 200:
            print("请求失败：%d  %s" % (response.status, response.url))
            return
        try:
            nodes = response.xpath('//*[@id="app"]/div[2]/div[1]')
            for node in nodes:
                item = parse_item(node)
                detail = '%s%s' % (self.base_url, item['href'])
                exist = _get_video_detail(self.cursor, item['href'])
                if exist is False:
                    yield scrapy.Request(url=detail, meta={"item": item}, callback=self._detail, dont_filter=True)
        except Exception as e:
            print('数据解析出错：' + response.url + "**********" + e)

    def _detail(self, response: scrapy.http.HtmlResponse):
        if response.status != 200:
            print("请求失败：%d  %s" % (response.status, response.url))
            return
        item = parse_detail(response, response.meta["item"], self.cursor, self.base_url, self._detail,
                            _get_video_detail, self._create_spider)
        yield item

    def _update_page_status(self, url: str, status: int):
        _update = 'update `t_pages` set `status` = %d where `url` = "%s"' % (status, url)
        try:
            self.cursor.execute(_update)
            self.db.commit()
        except pymysql.MySQLError as _:
            print("更新页面状态错误")

    @staticmethod
    def _create_spider(exist, base_url: str, detail, item: GtvVideoItem):
        if exist is False:
            _url = '%s%s' % (base_url, item['href'])
            yield scrapy.Request(url=_url, meta={"item": item}, callback=detail, dont_filter=True)
