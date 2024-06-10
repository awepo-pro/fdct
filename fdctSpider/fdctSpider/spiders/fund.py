import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import FundItem

class fundPySpider(CrawlSpider):
    name = "fund.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/']

    page_pattern = r'/zh_tw/fund_information.*'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse', follow=True)
    ]

    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/zh_tw/fund_information_detail/article/lvm7ejtv.html']
    #     return [scrapy.Request(url=url, callback=self.parse) for url in start_urls]

    def parse(self, response):
        fund = FundItem()
        fund['url'] = response.url

        container = response.css('div.acticle-div')
        fund['title'] = container.css('span ::text').extract_first()
        fund['article'] = container.css('div.details_body div span span ::text').extract()
        # all_text = container.xpath('//text()').extract()
        # all_text = ''.join(all_text).strip()
        fund['date'] = container.xpath('//div[1]/span[2]/text()').extract()

        return fund
