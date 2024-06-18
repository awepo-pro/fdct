import scrapy
from ..items import FundItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class Fund2PySpider(CrawlSpider):
    name = "fund"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ["https://www.fdct.gov.mo/zh_tw/fund_information_detail/article/"]
    
    rules = [
        Rule(LinkExtractor(allow=r'\w*\.html'), callback='parse_item')
    ]
    
    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/zh_tw/fund_information_detail/article/k71ydtch.html']
    #     return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]

    
    def __extract_article(self, response):
        return response.xpath('//div[@class="acticle-div"]//div[@class="details_body"]/descendant-or-self::*/text()').extract()

    def parse_item(self, response):
        fund = FundItem()

        # `acticle` spelling mistake in the webpage
        fund['url'] = response.url
        fund['title'] = response.css('.acticle-div span ::text').extract_first()
        fund['article'] = self.__extract_article(response) # return an empty list if nth found
        fund['date'] = response.xpath('//div[@class="acticle-div"]/div[1]/span[2]/text()').extract()

        yield fund
