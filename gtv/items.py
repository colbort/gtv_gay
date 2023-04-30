# -*- coding: utf-8 -*-
import scrapy


class GtvCateItem(scrapy.Item):
    href = scrapy.Field()
    zh_tw = scrapy.Field()
    count = scrapy.Field()
    zh_cn = scrapy.Field()

    # def __repr__(self):
    #     return repr((self.href, self.title, self.count))


class GtvVideoItem(scrapy.Item):
    url = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    cover = scrapy.Field()
    image = scrapy.Field()
    date = scrapy.Field()
    views = scrapy.Field()
    comments = scrapy.Field()
    category = scrapy.Field()
    recommend = scrapy.Field()
    categories = scrapy.Field()

    # def __repr__(self):
    #     return repr((self.url., self.href, self.title, self.cover, self.image, self.date, self.views,
    #                  self.comments, self.category, self.recommend))


class CategoryItem(object):
    id = -1
    zh_tw = ""
    zh_cn = ""
    href = ""
    count = 0

    def __init__(self, data: tuple):
        if len(data) != 5:
            return
        else:
            self.id = data[0]
            self.zh_tw = data[1]
            self.zh_cn = data[2]
            self.href = data[3]
            self.count = data[4]


class HalfItem(object):
    id = -1
    href = ""

    def __init__(self, data: tuple):
        if len(data) != 2:
            return
        else:
            self.id = data[0]
            self.href = data[1]
