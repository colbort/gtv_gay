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
                self.start_urls.append('%s%s' % (self.base_url, row[3]))
        except Exception as e:
            print("获取视频分类错误: ", e)
        pass

    def parse(self, response: scrapy.http.HtmlResponse):
        if response.status != 200:
            print("请求失败：%d  %s" % (response.status, response.url))
            return
        try:
            _size = response.xpath('//*[@id="app"]/div[2]/div[3]/nav/div/div[1]/p/span[2]/text()').get()

            _total = response.xpath('//*[@id="app"]/div[2]/div[3]/nav/div/div[1]/p/span[3]/text()').get()
            print(_total)
        except Exception as e:
            print('数据解析出错：' + response.url + "**********" + e)
