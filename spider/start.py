from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import sys

class BocCrawler():
    def __init__(self):
        scrapy_settings = get_project_settings()
        self.process = CrawlerProcess(scrapy_settings)

    def start(self):
        self.process.crawl('ratejp')
        self.process.start()

def main(args):
    crawler = BocCrawler()
    crawler.start()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
