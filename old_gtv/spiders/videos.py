import json

import js2py
import js2xml
import pymysql
import scrapy
from lxml import etree

from old_gtv.items import GtvVideoItem
from old_gtv.settings import *


class GtvVideosSpider(scrapy.Spider):
    name = 'videos'
    allowed_domains = ['danlanshipin.gay/old_gtv']
    base_url = "https://dlsp.gay"
    # start_urls = ['https://dlsp.gay/gtv/cate/%E6%A0%A1%E5%9B%AD']
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
            select = "select * from cates"
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
            for row in rows:
                self.start_urls.append('%s%s' % (self.base_url, row[2]))
        except Exception as e:
            print(e)
        pass

    def parse(self, response: scrapy.http.HtmlResponse):
        try:
            nodes = response.xpath('//*[@id="app"]/div[2]/div[2]/div')
            for node in nodes:
                item = _parse_item(node)
                detail = '%s%s' % (self.base_url, item['href'])
                exist = self._get_video_detail(item['href'])
                if exist:
                    print('视频详情已存在 = %s' % item['href'])
                else:
                    yield scrapy.Request(url=detail, meta={"item": item}, callback=self._detail, dont_filter=True)
            try:
                url = response.xpath('//*[@id="app"]/div[2]/div[3]/nav/div/div[2]/span/a[@rel="next"]/@href').get()
                if url is not None:
                    yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            except Exception as e:
                print('下载完成：' + e + response.url)
        except Exception as e:
            print('数据解析出错：' + response.url + "**********" + e)

    @staticmethod
    def _detail(response: scrapy.http.HtmlResponse):
        item = response.meta["item"]
        info = response.xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div[@class="text-sm"]/div')

        for it in info:
            label = it.xpath('text()').get()
            item['views'] = 0
            item['comments'] = 0
            if label.count('播放次數:') > 0:
                item['views'] = int(it.xpath('span/text()').get())
            elif label == ' 評論: ':
                item['comments'] = int(it.xpath('span/text()').get())
        cats = response.xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div[@class="p-2 my-2 '
                              'border border-indigo-400 border-dashed"]')
        category = []
        for cate in cats:
            label = cate.xpath('span/text()').get()
            try:
                if label.index('分類:') >= 0:
                    for e in cate.xpath('a'):
                        category.append(e.xpath('text()').get())
            except ValueError as _:
                continue
        item['category'] = json.dumps(category, ensure_ascii=False)
        item['categories'] = category

        recs = response.xpath('//*[@id="app"]/div[2]/div[2][@class="w-full"]/div')
        recommend = []
        for it in recs.xpath('div'):
            recommend.append(_parse_item(it))
        # item['recommend'] = json.dumps(recommend, default=lambda o: o.__dict__, ensure_ascii=False).strip()
        json_str = json.dumps(recommend, default=lambda o: o.__dict__, ensure_ascii=False).strip()
        arrays = json.loads(json_str)
        objects = []
        for e in arrays:
            objects.append(e['_values'])
        item['recommend'] = json.dumps(objects)

        js = response.xpath('//*[@id="app"]/div[2]/div[1]/div[1]/div/div[1]/div[1]/script/text()').get().split('\n')
        for row in js:
            try:
                if row.index('window.video_url = ') >= 0:
                    item['url'] = row.replace('window.video_url = ', '').replace(';', '').replace('"', '').strip()
            except ValueError as _:
                # print(row)
                continue
        for row in js:
            try:
                if row.index('window.video_cover = ') >= 0:
                    # print(row)
                    item['cover'] = row.replace('window.video_cover = ', '').replace(';', '').replace("'", '').strip()
            except ValueError as _:
                # print(row)
                continue
        # print(item)
        yield item

    def _get_video_detail(self, href):
        try:
            select = "select * from videos where href=%s"
            self.cursor.execute(select, href)
            row = self.cursor.fetchone()
            if row is not None:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


def _parse_item(node):
    item = GtvVideoItem()
    item["href"] = node.xpath('a/@href').get().strip().replace('\n', '').replace('\r', '')
    item["image"] = node.xpath('a/img/@data-src').get().strip().replace('\n', '').replace('\r', '')
    item["title"] = node.xpath('a/img/@alt').get().strip().replace('\n', '').replace('\r', '')
    item["date"] = node.xpath('a/div/text()').get().strip().replace('\n', '').replace('\r', '')
    return item
