from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import BulletinItem


class BulletinPySpider(CrawlSpider):
    name = "bulletin_detail"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw/bulletin_detail/article/', 'https://www.fdct.gov.mo/pt/bulletin_detail/article/', 'https://www.fdct.gov.mo/en/bulletin_detail/article/']

    page_pattern = r'\w*\.html'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse_item')
    ]
    
    def parse_item(self, response):
        detail = BulletinItem()

        detail['url'] = response.url
        detail['title'] = response.xpath('//div[@section-id="2835"]/div/div[1]//text()').extract()
        detail['article'] = response.xpath('//div[@section-id="2835"]//div[@class="acticle-div"]//text()').extract()

        yield detail
