# -*- coding: utf-8 -*-
import scrapy
from spider.items import Rate

import datetime
import logging

class RatejpSpider(scrapy.Spider):
    name = "ratejp"
    allowed_domains = ["srh.bankofchina.com"]


    def __init__(self, lasttime):
        self.lasttime = lasttime

    def start_requests(self):
        yield scrapy.Request(
            'http://srh.bankofchina.com/search/whpj/search.jsp'
            '?erectDate=&nothing=&pjname=1323',
            callback=self.parse_page)
    
    def parse_page(self, response):
        row_path = '//div[@class="BOC_main publish"]/table/tr[position()>1 and position()<last()]'

        for rate_row in response.xpath(row_path):
            timestamp = self.pub_time_from_row(rate_row)

            if timestamp <= self.lasttime:
                break
            
            rate = Rate()

            rate['currency'] = 'JPY'
            rate['tele_buy'] = self.tele_buy_from_row(rate_row)
            rate['cash_buy'] = self.cash_buy_from_row(rate_row)
            rate['tele_sell'] = self.tele_sell_from_row(rate_row)
            rate['cash_sell'] = self.cash_sell_from_row(rate_row)
            rate['middle'] = self.middle_from_row(rate_row)
            rate['pub_time'] = timestamp

            yield rate

    def tele_buy_from_row(self, row):
        price = row.xpath('./td[2]/text()').extract_first()
        return float(price)

    def cash_buy_from_row(self, row):
        price = row.xpath('./td[3]/text()').extract_first()
        return float(price)

    def tele_sell_from_row(self, row):
        price = row.xpath('./td[4]/text()').extract_first()
        return float(price)

    def cash_sell_from_row(self, row):
        price = row.xpath('./td[5]/text()').extract_first()
        return float(price)

    def middle_from_row(self, row):
        price = row.xpath('./td[7]/text()').extract_first()
        return float(price)

    def pub_time_from_row(self, row):
        time = row.xpath('./td[8]/text()').extract_first()
        (date, time) = tuple(time.strip().split())
        return self.get_datetime(date, time)

    def get_datetime(self, date_string, time_string):
        (year, month, day) = tuple(map(int, date_string.split('.')))
        date = datetime.date(year, month, day)

        cst = datetime.timezone(datetime.timedelta(hours=8), 'Asia/Shanghai')
        (h, m, s) = tuple(map(int, time_string.split(':')))
        time = datetime.time(h, m, s, 0, cst)

        return datetime.datetime.combine(date, time)
