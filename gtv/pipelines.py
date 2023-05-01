# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from zhconv import convert

from .items import *
from .settings import *


class GtvPipeline(object):
    def __init__(self):
        self.db = None
        self.cursor = None
        self.categories = []

    def open_spider(self, spider):
        print("*********************************************************************")
        print("启动爬虫")
        print("*********************************************************************")
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
        self._load_categories()

    def process_item(self, item, spider):
        if type(item) is GtvCateItem:
            self._cate_item(item)
        elif type(item) is GtvVideoItem:
            self._video_item(item)

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def _cate_item(self, item):
        _select = 'select * from t_categories where zh_tw=%s'
        try:
            self.cursor.execute(_select, [item['zh_tw']])
            one = self.cursor.fetchone()
            if one is not None:
                _sql = 'update t_categories set `href`="%s", `count`=%d, `zh_cn`="%s" where `zh_tw`="%s"' % (
                    item["href"], item['count'], item['zh_cn'], item["zh_tw"])
            else:
                _sql = 'insert into t_categories (`href`, `count`, `zh_tw`, `zh_cn`) values ("%s", %d, "%s", "%s")' % (
                    item["href"], item['count'], item["zh_tw"], item["zh_cn"])
            self.cursor.execute(_sql)
            self.db.commit()
        except pymysql.MySQLError as _:
            print("保存视频分类失败：" % _sql)
        return item

    def _video_item(self, item: GtvVideoItem):
        _save = self._save_video_item(item)
        self._save_video_detail_item(item)
        if _save:
            self._insert_index_to_c_v(item['categories'], item['href'])

    def _save_video_item(self, item: GtvVideoItem) -> bool:
        _select = 'select * from t_videos where href="%s"' % item['href']
        _exist = None
        try:
            self.cursor.execute(_select)
            _exist = self.cursor.fetchone()
        except pymysql.MySQLError as _:
            print("从 t_videos 获取数据失败：", _select)
            return False
        _temp = ''
        _save = False
        if _exist is not None:
            _temp = 'update t_videos set `title`="%s", `cover`="%s", `image`="%s",' \
                    ' `date`="%s", `views`=%d, `comments`=%d, `category`="%s" where `href`="%s"'
        else:
            _temp = 'insert into t_videos (`title`, `cover`, `image`, `date`, `views`, `comments`, ' \
                    '`category`, `href`) values ("%s", "%s", "%s", "%s", %d, %d, ' \
                    '"%s", "%s")'
            _save = True
        _sql = _temp % (item["title"], item['cover'], item['image'], item['date'], item['views'],
                        item['comments'], item['category'].replace('"', '\\"'), item['href'])
        try:
            self.cursor.execute(_sql)
            self.db.commit()
        except pymysql.MySQLError as _:
            return False
        return _save

    def _save_video_detail_item(self, item: GtvVideoItem):
        _select = 'select * from t_videos_detail where href="%s"' % item['href']
        try:
            self.cursor.execute(_select)
            _exist = self.cursor.fetchone()
        except pymysql.MySQLError as _:
            print("从 t_videos_detail 获取数据失败：", _select)
            return
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

    def _load_categories(self):
        _select = 'select * from `t_categories`'
        self.cursor.execute(_select)
        rows = self.cursor.fetchall()
        for row in rows:
            self.categories.append(CategoryItem(row))
        print("获取视频分类成功：", len(self.categories))

    def _get_id_by_zh_cn(self, zh_cn: str):
        for e in self.categories:
            if e.zh_cn == convert(zh_cn, 'zh-hans'):
                return e.id
        return 1000000

    def _insert_index_to_c_v(self, categories: [], href: str):
        _sql = 'insert into `t_index_c_v` (`cid`, `href`) values (%d, "%s")'
        _values = []
        for e in categories:
            _cid = self._get_id_by_zh_cn(e.replace("#", ""))
            _insert = _sql % (_cid, href)
            try:
                self.cursor.execute(_insert)
                self.db.commit()
            except pymysql.MySQLError as _:
                print("插入index_c_v错误：" + _insert)

