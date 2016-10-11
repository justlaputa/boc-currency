# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from influxdb import InfluxDBClient
import logging

class InfluxdbPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.influxdbClient = InfluxDBClient(host='localhost', port=8086,
                                             database='bocrate')
        
    def process_item(self, item, spider):

        points = []
        for t in ['tele_buy', 'cash_buy', 'tele_sell', 'cash_sell', 'middle']:
            point = {
                'measurement': 'jpyrate',
                'tags': {
                    'type': t
                },
                'time': item['pub_time'],
                'fields': {
                    'value': item[t]
                }
            }
            logging.debug('make point: %s ', point)
            
            points.append(point)

        self.influxdbClient.write_points(points)
        return item
