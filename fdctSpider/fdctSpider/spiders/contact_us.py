import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import ContactItem


class BulletinPySpider(CrawlSpider):
    name = "contact_us.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']

    page_pattern = r'^https://www.fdct.gov.mo/(zh_tw|pt|en)/contact_us*\.html'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse_item')
    ]

    def parse_item(self, response):
        contact = ContactItem()

        contact['url'] = response.url
        contact['title'] = response.css('.content div.content-title ::text').extract_first()
        contact['article'] = response.css('.content .content-body .contact_us_left ::text').extract()

        yield contact
