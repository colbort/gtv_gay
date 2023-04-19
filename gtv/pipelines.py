# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.crawler import CrawlerProcess

from .items import *
from .settings import *
from .spiders.videos import GtvVideosSpider


class GtvPipeline(object):
    def __init__(self):
        self.db = None
        self.cursor = None

    def open_spider(self, spider):
        # 爬虫程序启动时，只执行一次，一般用于建立数据库连接
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        if type(item) is GtvCateItem:
            self._cate_item(item)
        elif type(item) is GtvVideoItem:
            self._video_item(item)

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def _cate_item(self, item):
        select = 'select * from cates where title=%s'
        sql = 'insert into cates (`href`, `count`, `title`) values ("%s", %d, "%s")' % (
            item["href"], item['count'], item["title"])
        try:
            self.cursor.execute(select, [item['title']])
            one = self.cursor.fetchone()
            if one is not None:
                sql = 'update cates set `href`="%s", `count`=%d where `title`="%s"' % (
                    item["href"], item['count'], item["title"])
            self.cursor.execute(sql)
            self.db.commit()
        finally:
            print("1111111111111111111111111111")
        return item

    def _video_item(self, item: GtvVideoItem):
        last_id = self._save_video_item(item)
        self._save_video_detail_item(item)
        if last_id is -1:
            return
        self._save_c_v_index(last_id, item['category'])

    def _save_video_item(self, item: GtvVideoItem) -> int:
        _select = 'select * from t_videos where href="%s"' % item['href']
        self.cursor.execute(_select)
        _exist = self.cursor.fetchone()
        _temp = ''
        if _exist is not None:
            _temp = 'update t_videos set `title`="%s", `cover`="%s", `image`="%s",' \
                    ' `date`="%s", `views`=%d, `comments`=%d, `category`="%s" where `href`="%s"'
        else:
            _temp = 'insert into t_videos (`title`, `cover`, `image`, `date`, `views`, `comments`, ' \
                    '`category`, `href`) values ("%s", "%s", "%s", "%s", %d, %d, ' \
                    '"%s", "%s")'
        _sql = _temp % (item["title"], item['cover'], item['image'], item['date'], item['views'],
                        item['comments'], item['category'].replace('"', '\\"'), item['href'])
        try:
            self.cursor.execute(_sql)
            self.db.commit()
        except pymysql.MySQLError as _:
            print("保存视频基本信息失败 %s" % item['href'])
            return -1
        return self.cursor.lastrowid

    def _save_video_detail_item(self, item: GtvVideoItem):
        _select = 'select * from t_videos_detail where href="%s"' % item['href']
        self.cursor.execute(_select)
        _exist = self.cursor.fetchone()
        _temp = ''
        if _exist is not None:
            _temp = 'update t_videos_detail set `url`="%s", `recommend`="%s" where `href`="%s"'
        else:
            _temp = 'insert into t_videos_detail (`url`, `recommend`, `href`) values ("%s", "%s", "%s")'
        _sql = _temp % (item['url'], item['recommend'].replace('"', '\\"').replace("'", ''), item['href'])
        try:
            self.cursor.execute(_sql)
            self.db.commit()
        except pymysql.MySQLError as _:
            print("保存视频详细信息失败 %s" % item['href'])

    def _save_c_v_index(self, vid, categories):
        cats = categories.split(',')
        for cate in cats:
            print(cate)
