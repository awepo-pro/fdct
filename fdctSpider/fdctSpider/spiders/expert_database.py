import scrapy
from ..items import CoopItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class ExpertSpider(CrawlSpider):
    name = "expert_database.py"
    allowed_domains = ["fdct.gov.mo"]
    
    def start_requests(self):
        start_urls = ['https://www.fdct.gov.mo/zh_tw/expert_database.html', 'https://www.fdct.gov.mo/pt/expert_database.html', 'https://www.fdct.gov.mo/en/expert_database.html']
        return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]


    def parse_item(self, response):
        expert = CoopItem()

        expert['url'] = response.url
        expert['title'] = response.css('.content-title ::text').extract()
        expert['article'] = response.xpath('//div[@class="content-body"]//span/text()').extract()

        yield expert
