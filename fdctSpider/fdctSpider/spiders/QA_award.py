# import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import QAAwardItem
# import json

class qa_format:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class BulletinPySpider(CrawlSpider):
    name = "QA_award.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']

    page_pattern = r'^https://www.fdct.gov.mo/(zh_tw|pt|en)/award\.html'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse_item')
    ]

    def parse_item(self, response):
        qa = QAAwardItem()

        qa['url'] = response.url
        qa['title'] = response.css('.content-title ::text').extract()

        qa['prizes'] = response.xpath('//div[@class="content-body"]//u//text()').extract()
        qa['question'] = response.xpath('//div[@class="content-body"]/span[@class="qa_question"]/text()').extract()
        qa['answer'] = response.xpath('//div[@class="content-body"]/span[@class="qa_answer"]/text()').extract()

        yield qa