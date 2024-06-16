# import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import BulletinItem


class BulletinPySpider(CrawlSpider):
    name = "bulletin.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']

    page_pattern = r'^https://www.fdct.gov.mo/(zh_tw|pt|en)/\w*\.html'
    deny_pattern = r'(faq|about|law|awards|video|cooperation|9|research_funding1)\.html'    # redirecting page and Q & A

    rules = [
        Rule(LinkExtractor(allow=page_pattern, deny=deny_pattern), callback='parse_item')
    ]

    def parse_item(self, response):
        bulletin = BulletinItem()
        container = response.css('div.content')

        bulletin['url'] = response.url
        bulletin['title'] = container.css('div.content-title ::text').extract_first()
        bulletin['article'] = container.css('div.content-body ::text').extract()

        yield bulletin
