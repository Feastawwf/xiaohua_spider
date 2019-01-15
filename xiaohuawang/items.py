# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuawangItem(scrapy.Item):
    # define the fields for your item here like:
    folder_name = scrapy.Field()      # 吉林大学
    img_url = scrapy.Field()         # jpg
    img_name = scrapy.Field()           # 请求的api  jpg
    # img_bytes = scrapy.Field()    b'\se\07\'


