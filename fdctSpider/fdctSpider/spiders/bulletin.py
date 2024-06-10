import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from fdctSpider.items import BulletinItem

class BulletinPySpider(CrawlSpider):
    name = "bulletin.py"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw', 'https://www.fdct.gov.mo/pt', 'https://www.fdct.gov.mo/en']

    page_pattern = r'^https://www\.fdct\.gov\.mo/pt/\w*\.html'

    rules = [
        Rule(LinkExtractor(allow=page_pattern), callback='parse', follow=True)
    ]


    # def start_requests(self):
    #     start_urls = ['https://www.fdct.gov.mo/en/macau_awards.html']
    #     return [scrapy.Request(url=url, callback=self.parse) for url in start_urls]

    def __language(self, str):
        lang = ''
        if r'/zh_tw/' in str:
            lang = 'zh'
        elif r'/pt/' in str:
            lang = 'pt'
        else:
            lang = 'en'

        return lang

    def parse(self, response):
        bulletin = BulletinItem()
        bulletin['url'] = response.url
        bulletin['lang'] = self.__language(bulletin['url'])

        container = response.css('div.content')
        bulletin['title'] = container.css('div.content-title ::text').extract_first()
        bulletin['article'] = container.css('div.content-body ::text').extract()

        return bulletin
