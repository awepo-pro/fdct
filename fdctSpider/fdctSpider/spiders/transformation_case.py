from ..items import CoopItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

class TransSpider(CrawlSpider):
    name = "transformation_case"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw/transformation_case_detail/article/', 'https://www.fdct.gov.mo/pt/transformation_case_detail/article/', 
                  'https://www.fdct.gov.mo/en/transformation_case_detail/article/']
    
    rules = [
        Rule(LinkExtractor(allow=r'\w*\.html'), callback='parse_item')
    ]
    
    def parse_item(self, response):
        trans = CoopItem()

        # `acticle` spelling mistake in the webpage
        trans['url'] = response.url
        target = response.css('.acticle-div span ::text').extract()
        trans['title'] = target[0]
        trans['date'] = target[1]
        trans['article'] = response.xpath('//div[@class="acticle-div"]/div[@class="details_body"]//span//text()').extract()

        yield trans
