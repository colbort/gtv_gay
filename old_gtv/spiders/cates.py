# -*- coding: utf-8 -*-
import scrapy
from old_gtv.items import GtvCateItem


class ItCastSpider(scrapy.Spider):
    name = 'cates'
    allowed_domains = ['danlanshipin.gay/old_gtv']
    start_urls = ['http://danlanshipin.gay/gtv/cates']

    def parse(self, response):
        for node in response.xpath('//*[@id="app"]/div[2]/div[2]/div'):
            item = GtvCateItem()
            item['title'] = node.xpath('h4/a/text()').get()
            item['count'] = int(node.xpath('h4/small/text()').get().replace('(', "").replace(')', ""))
            item['href'] = node.xpath('h4/a/@href').get()
            yield item
