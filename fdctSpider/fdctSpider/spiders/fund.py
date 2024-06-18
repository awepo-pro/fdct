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
    
    def parse_item(self, response):
        fund = FundItem()

        # `acticle` misspell in the webpage tag name
        fund['url'] = response.url
        fund['title'] = response.css('.acticle-div span ::text').extract_first()
        fund['article'] = response.xpath('//div[@class="acticle-div"]//div[@class="details_body"]/descendant-or-self::*/text()').extract()
        fund['date'] = response.xpath('//div[@class="acticle-div"]/div[1]/span[2]/text()').extract()

        yield fund
