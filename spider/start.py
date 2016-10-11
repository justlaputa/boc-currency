from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from influxdb import InfluxDBClient

from datetime import datetime, timezone
import sys
import logging

class BocCrawler():
    def __init__(self):
        scrapy_settings = get_project_settings()
        self.process = CrawlerProcess(scrapy_settings)

        influxClient = InfluxDBClient(host='localhost', port=8086, database='bocrate')
        rs = influxClient.query('select * from jpyrate order by time desc limit 1')
        jpy_points = list(rs.get_points())

        if len(jpy_points) == 0:
            self.last_timestamp = datetime.fromtimestamp(0, timezone.utc)
        else:
            self.last_timestamp = jpy_points(0)['time']

    def start(self):
        self.process.crawl('ratejp', lasttime = self.last_timestamp)
        self.process.start()

def main(args):
    crawler = BocCrawler()
    crawler.start()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
