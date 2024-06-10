import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import FundItem

class fundPySpider(CrawlSpider):
    name = "fund.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']

    page_pattern = r'/fund_information.*'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse', follow=True)
    ]


    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/pt/fund_information_detail/article/lwinrol8.html']
    #     return [scrapy.Request(url=url, callback=self.parse) for url in start_urls]

    def __extract_article(self, container):
        container = container.css('div.details_body')

        if container.css('div') is not None:
            container = container.css('div')
        if container.css('span'):
            container = container.css('span')    

        if container.css('span'):
            container = container.css('span')

        return container.css('::text').extract()

    def parse(self, response):
        fund = FundItem()
        fund['url'] = response.url

        if r'/zh_tw/' in fund['url']:
            fund['lang'] = 'zh'
        elif r'/pt/' in fund['url']:
            fund['lang'] = 'pt'
        else:
            fund['lang'] = 'en'

        container = response.css('div.acticle-div')
        fund['title'] = container.css('span ::text').extract_first()
        # fund['article'] = container.css('div.details_body div span span ::text').extract()
        fund['article'] = self.__extract_article(container)
        # all_text = container.xpath('//text()').extract()
        # all_text = ''.join(all_text).strip()
        fund['date'] = container.xpath('//div[1]/span[2]/text()').extract()

        return fund
