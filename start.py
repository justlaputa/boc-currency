from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from datetime import datetime, timezone, timedelta
import iso8601
import sys
import os
import logging

from google.cloud import bigquery

LOGLEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

class BocCrawler():
    def __init__(self):
        scrapy_settings = get_project_settings()
        self.process = CrawlerProcess(scrapy_settings)

        self.bq_client = bigquery.Client()
        self.last_timestamp = self.get_last_timestamp()

    def get_last_timestamp(self):
        last_record = self.get_latest_record()

        if last_record is None:
            return datetime.fromtimestamp(0, timezone.utc)

        logging.info('latest record: {}'.format(last_record))
        return last_record['timestamp']

    def get_latest_record(self):
        query = (
            "SELECT timestamp FROM `personal-finance-228402.exchange_rate.boc` "
            "ORDER BY timestamp DESC "
            "LIMIT 1"
        )

        query_job = self.bq_client.query(
            query,
            location = 'US',
        )

        result = query_job.result()
        if result.total_rows > 0:
            return list(result)[0]
        return None

    def start(self):
        print('last time: {}'.format(self.last_timestamp))
        self.process.crawl('ratejp', lasttime = self.last_timestamp)
        self.process.start()

def main(args):
    try:
        crawler = BocCrawler()
        crawler.start()
    except Exception:
        logging.error('failed to run crawler', exc_info=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
