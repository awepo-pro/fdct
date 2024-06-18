import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import FileItem
from ..tool.println import println

class ImagesPySpider(CrawlSpider):
    name = "files"
    allowed_domains = ["www.fdct.gov.mo"]

    def start_requests(self):
        start_urls = ['https://www.fdct.gov.mo/files/', 'https://www.fdct.gov.mo/files/laws_and_regulations/']
        
        for yr in range(2014, 2023):
            start_urls.append(f'https://www.fdct.gov.mo/files/FDCTyearbook/cn/{yr}/')
            start_urls.append(f'https://www.fdct.gov.mo/files/FDCTyearbook/pt/{yr}/')
            
        return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]

    def __is_files(self, link):
        return link.endswith('.pdf') or link.endswith('.jpg')

    def parse_item(self, response):
        file = FileItem()
        println(response.url, 'warning')

        Links = response.xpath('//table//a//@href').extract()
        # file['path'] = self.__remove_necessary(Links)
        file['file_urls'] = [response.urljoin(link) for link in Links if self.__is_files(link)]

        yield file