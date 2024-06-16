import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import FundItem

class fundPySpider(CrawlSpider):
    name = "fund.py"

    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']
    
    page_pattern = r'/fund_information_detail/.*'
    
    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse_item'),
    ]

    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/zh_tw/fund_information_detail/article/lvm7ejtv.html']
        # return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]

    def __extract_article(self, container):
        return container.xpath('//div[@class="details_body"]/descendant-or-self::*/text()').extract()

    def parse_item(self, response):
        fund = FundItem()

        # `acticle` spelling mistake in the webpage
        container = response.css('.acticle-div')
        article = self.__extract_article(container)

        fund['url'] = response.url
        fund['title'] = container.css('span ::text').extract_first()
        fund['article'] = article
        fund['date'] = container.xpath('//div[1]/span[2]/text()').extract()

        yield fund
