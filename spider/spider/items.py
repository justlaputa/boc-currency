# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Rate(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    currency = scrapy.Field()
    tele_buy = scrapy.Field()
    cash_buy = scrapy.Field()
    tele_sell = scrapy.Field()
    cash_sell = scrapy.Field()
    middle = scrapy.Field()
    pub_time  = scrapy.Field()
