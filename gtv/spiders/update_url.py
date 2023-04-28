import json

import pymysql
import scrapy

from gtv.items import GtvVideoItem, HalfItem
from gtv.settings import *


class GtvVideosSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['danlanshipin.gay/old_gtv']
    base_url = "https://www.xlsp.fun"
    # start_urls = ['https://www.xlsp.fun/gtv/cate/%E5%85%B5%E5%93%A5%E5%93%A5']
    start_urls = ['https://www.xlsp.fun/gtv/9486']

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
        # try:
        #     _select = 'select `id`, `href` from `videos`'
        #     self.cursor.execute(_select)
        #     rows = self.cursor.fetchall()
        #     for row in rows:
        #         self.start_urls.append(self.base_url + HalfItem(row).href)
        # except Exception as e:
        #     print(e)
        # pass

    def parse(self, response: scrapy.http.HtmlResponse):
        if response.status != 200:
            print("请求错误：", response.status)
            return
        try:
            js = response.xpath('//*[@id="app"]/div[2]/div[1]/div[1]/div/div[1]/div[1]/script/text()').get().split('\n')
            for row in js:
                try:
                    if row.index('window.video_url = ') >= 0:
                        _url = row.replace('window.video_url = ', '').replace(';', '').replace('"', '').strip()
                        print(_url)
                except ValueError as _:
                    continue
        except Exception as e:
            print('数据解析出错：' + response.url + "**********" + e)

