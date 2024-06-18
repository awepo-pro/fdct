import scrapy
import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import ImageItem

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ImagesPySpider(CrawlSpider):
    name = "_images.py"
    allowed_domains = ["www.fdct.gov.mo"]

    start_urls = ["https://www.fdct.gov.mo/images"]

    dir_pattern = r'.*/$'
    
    rules = [
        Rule(LinkExtractor(allow=dir_pattern), callback='parse_item') # fetch all directories instead of files
    ]

    downloadPath = os.getcwd() + 'images'

    # add this in pipelines.py in refactoring
    # remove all folder' paths 
    def __remove_necessary(self, links):
        path = []
        desired_format = ['.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.pdf']

        for link in links:
            for suffix in desired_format:
                if link.endswith(suffix):
                    path.append(self.url + link)
                    break

        return path

    def parse_item(self, response):
        images = ImageItem()
        self.url = response.url

        Links = response.css('a::attr(href)').extract()
        images['path'] = self.__remove_necessary(Links)

        yield images