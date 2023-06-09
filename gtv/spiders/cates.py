# -*- coding: utf-8 -*-
import scrapy
from gtv.items import GtvCateItem
from zhconv import convert


class ItCastSpider(scrapy.Spider):
    name = 'cates'
    allowed_domains = ['danlanshipin.gay/old_gtv']
    start_urls = ['https://www.xlsp.fun/gtv/cates']

    def parse(self, response):
        for node in response.xpath('//*[@id="app"]/div[2]/div[2]/div'):
            item = GtvCateItem()
            item['zh_tw'] = node.xpath('h4/a/text()').get()
            item['count'] = int(node.xpath('h4/small/text()').get().replace('(', "").replace(')', ""))
            href = node.xpath('h4/a/@href').get()
            item['href'] = href
            item['zh_cn'] = convert(href.replace('/gtv/cate/', ''), 'zh-hans')
            yield item
