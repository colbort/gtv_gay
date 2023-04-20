import scrapy


class GtvCateItem(scrapy.Item):
    href = scrapy.Field()
    title = scrapy.Field()
    count = scrapy.Field()

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
