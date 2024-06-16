import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import DownloadItem

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ImagesPySpider(CrawlSpider):
    name = "download.py"
    allowed_domains = ["www.fdct.gov.mo"]

    start_urls = ["https://www.fdct.gov.mo/download"]

    dir_pattern = r'.*/$'
    deny_pattern = r'App/'
    
    rules = [
        Rule(LinkExtractor(allow=dir_pattern, deny=deny_pattern), callback='parse_item')    # go to all directories instead of files
    ]

    # add this in pipelines.py in refactoring
    def __remove_necessary(self, links):
        path = []
        desired_format = ['.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.pdf', '.ppsx', '.webp', '.docx', '.doc']

        for link in links:
            for suffix in desired_format:
                if link.endswith(suffix):
                    path.append(self.url + link)
                break

        return path

    def parse_item(self, response):
        download = DownloadItem()
        self.url = response.url

        Links = response.css('a::attr(href)').extract()
        download['path'] = self.__remove_necessary(Links)

        yield download