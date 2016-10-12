from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from influxdb import InfluxDBClient

from datetime import datetime, timezone
import iso8601
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
            tz_sh = datetime.timezone(datetime.timedelta(hours=8), 'Asia/Shanghai')

            self.last_timestamp = iso8601.parse_date(jpy_points[0]['time'])
            logging.info('latest updated timestamp: %s',
                         self.last_timestamp.astimezone(tz_sh))

    def start(self):
        self.process.crawl('ratejp', lasttime = self.last_timestamp)
        self.process.start()

def main(args):
    crawler = BocCrawler()
    crawler.start()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
