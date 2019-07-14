# -*- coding: utf-8 -*-
import scrapy
from spider.items import Rate

import datetime
import logging

class RatejpSpider(scrapy.Spider):
    name = "ratejp"
    allowed_domains = ["srh.bankofchina.com"]
    finished_flg = False

    def __init__(self, lasttime=datetime.datetime.utcfromtimestamp(0)):
        self.lasttime = lasttime

    def start_requests(self):
        yield scrapy.Request(
            'http://srh.bankofchina.com/search/whpj/search.jsp'
            '?erectDate=&nothing=&pjname=1323&page=1',
            callback=self.parse_page)
    
    def parse_page(self, response):
        if self.is_over_last_page(response):
            logging.info('pass the last page, exit')
            return
        
        row_path = '//div[@class="BOC_main publish"]/table/tr[position()>1 and position()<last()]'

        for rate_row in response.xpath(row_path):
            timestamp = self.pub_time_from_row(rate_row)

            if timestamp <= self.lasttime:
                logging.info('reach the latest record, stop parsing')
                self.finished_flg = True
                break
            
            rate = Rate()

            rate['timestamp'] = timestamp
            rate['currency'] = 'JPY'
            rate['ex_buy'] = self.ex_buy_from_row(rate_row)
            rate['cash_buy'] = self.cash_buy_from_row(rate_row)
            rate['ex_sell'] = self.ex_sell_from_row(rate_row)
            rate['cash_sell'] = self.cash_sell_from_row(rate_row)
            rate['middle'] = self.middle_from_row(rate_row)

            yield rate

        if not self.finished_flg:
            logging.info('continue to go to next page')
            url_page = self.get_page_no_from_url(response.url)

            i = response.url.find('page=')
            if i == -1:
                next_url = response.url + 'page=%d' % (url_page+1)
            else:
                next_url = response.url[0:i] + 'page=%d' % (url_page+1)
            
            yield scrapy.Request(next_url, callback=self.parse_page)

    def is_over_last_page(self, response):
        url_page = self.get_page_no_from_url(response.url)

        max_page = int(response.xpath('//form[@name="pageform"]/input[@name="page"]/@value').extract_first())

        return url_page > max_page

    def get_page_no_from_url(self, url):
        i = url.find('page=')
        if i == -1:
            return 1
        else:
            return int(url[i+5:])

    def ex_buy_from_row(self, row):
        price = row.xpath('./td[2]/text()').extract_first()
        return float(price)

    def cash_buy_from_row(self, row):
        price = row.xpath('./td[3]/text()').extract_first()
        return float(price)

    def ex_sell_from_row(self, row):
        price = row.xpath('./td[4]/text()').extract_first()
        return float(price)

    def cash_sell_from_row(self, row):
        price = row.xpath('./td[5]/text()').extract_first()
        return float(price)

    def middle_from_row(self, row):
        price = row.xpath('./td[6]/text()').extract_first()
        return float(price)

    def pub_time_from_row(self, row):
        time = row.xpath('./td[7]/text()').extract_first()
        (date, time) = tuple(time.strip().split())
        return self.get_datetime(date, time)

    def get_datetime(self, date_string, time_string):
        (year, month, day) = tuple(map(int, date_string.split('.')))
        date = datetime.date(year, month, day)

        cst = datetime.timezone(datetime.timedelta(hours=8), 'Asia/Shanghai')
        (h, m, s) = tuple(map(int, time_string.split(':')))
        time = datetime.time(h, m, s, 0, cst)

        return datetime.datetime.combine(date, time)
