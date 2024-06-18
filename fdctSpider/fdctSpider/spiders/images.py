import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import ImageItem
from ..tool.println import println

class ImagesPySpider(CrawlSpider):
    name = "images"
    allowed_domains = ["www.fdct.gov.mo"]
    
    def start_requests(self):
        start_urls = ['https://www.fdct.gov.mo/images', 'https://www.fdct.gov.mo/images/about/', 'https://www.fdct.gov.mo/images/awards/', 'https://www.fdct.gov.mo/images/funding/', 'https://www.fdct.gov.mo/images/fund-information/', 'https://www.fdct.gov.mo/images/icon/', 'https://www.fdct.gov.mo/images/information/', 'https://www.fdct.gov.mo/images/propaganda/', 'https://www.fdct.gov.mo/images/speech/', 'https://www.fdct.gov.mo/images/rotate_images/', 'https://www.fdct.gov.mo/images/summer_camp/', 'https://www.fdct.gov.mo/images/wind/']        
        return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]

    def parse_item(self, response):
        file = ImageItem()
        println(response.url, 'warning')

        Links = response.xpath('//table//a//@href').extract()
        file['image_urls'] = [response.urljoin(link) for link in Links if not link.endswith('/')]

        yield file