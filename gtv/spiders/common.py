# -*- coding: utf-8 -*-
import json

import scrapy

from gtv.items import GtvVideoItem


def parse_item(node):
    item = GtvVideoItem()
    item["href"] = node.xpath('a/@href').get().strip().replace('\n', '').replace('\r', '')
    item["image"] = node.xpath('a/img/@data-src').get().strip().replace('\n', '').replace('\r', '')
    item["title"] = node.xpath('a/img/@alt').get().strip().replace('\n', '').replace('\r', '')
    item["date"] = node.xpath('a/div/text()').get().strip().replace('\n', '').replace('\r', '')
    return item


def parse_detail(response: scrapy.http.HtmlResponse, item: GtvVideoItem, cursor, base_url: str, detail,
                 get_video_detail, scrapy_request):
    _info = response.xpath('//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div[@class="text-sm"]/div')

    try:
        for it in _info:
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
            _item = parse_item(it)
            # 暂时注释掉
            # exist = get_video_detail(cursor, _item['href'])
            # if exist is False:
            #     scrapy_request(exist, base_url, detail, _item)
            recommend.append(dict(_item))
        item['recommend'] = json.dumps(recommend, default=lambda o: o.__dict__, ensure_ascii=False).strip()
        js = response.xpath('//*[@id="app"]/div[2]/div[1]/div[1]/div/div[1]/div[1]/script/text()').get().split('\n')
        for row in js:
            try:
                if row.index('window.video_url = ') >= 0:
                    item['url'] = row.replace('window.video_url = ', '').replace(';', '').replace('"', '').strip()
            except ValueError as _:
                continue
        for row in js:
            try:
                if row.index('window.video_cover = ') >= 0:
                    item['cover'] = row.replace('window.video_cover = ', '').replace(';', '').replace("'", '').strip()
            except ValueError as _:
                continue

        return item
    except Exception as e:
        print("数据解析错误：%v" % e)
