import scrapy
from ..items import CoopItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class MainlandCoopSpider(CrawlSpider):
    name = "mainland_coop.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw/mainland_macau_cooperation_detail/article/', 'https://www.fdct.gov.mo/pt/mainland_macau_cooperation_detail/article/', 'https://www.fdct.gov.mo/en/mainland_macau_cooperation_detail/article/']
    
    rules = [
        Rule(LinkExtractor(allow=r'\w*\.html'), callback='parse_item')
    ]
    
    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/zh_tw/fund_information_detail/article/k71ydtch.html']
    #     return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]


    def parse_item(self, response):
        coop = CoopItem()

        coop['url'] = response.url
        target = response.css('.acticle-div span ::text').extract()
        coop['title'] = target[0]
        coop['date'] = target[1]
        coop['article'] = response.xpath('//div[@class="acticle-div"]/div[@class="details_body"]//span//text()').extract()

        yield coop