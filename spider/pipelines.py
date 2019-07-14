# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from google.cloud import bigquery

class BigQueryPipeline(object):

    def __init__(self):
        self.rows = []

    def open_spider(self, spider):
        self.bq_client = bigquery.Client()
        dataset_ref = self.bq_client.dataset('exchange_rate')
        table_ref = dataset_ref.table('boc')

        try:
            self.table = self.bq_client.get_table(table_ref)
        except Exception:
            logging.error('bigquery table not found')
            raise

    def process_item(self, item, spider):
        self.rows.append(dict(item))
        return item

    def close_spider(self, spider):
        if len(self.rows) <= 0:
            logging.info('no record to send, we are done')
            return

        logging.info('sending %d records to bigquery', len(self.rows))
        errors = self.bq_client.insert_rows(self.table, self.rows)
        if len(errors) > 0:
            logging.warning('errors while inserting records to bigquery: {}'.format(errors))
