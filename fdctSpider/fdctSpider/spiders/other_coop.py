from ..items import CoopItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class OtherCoopSpider(CrawlSpider):
    name = "other_coop"
    allowed_domains = ["fdct.gov.mo"]
    start_urls = ['https://www.fdct.gov.mo/zh_tw/other_cooperation_details/article/', 'https://www.fdct.gov.mo/pt/other_cooperation_details/article/', 
                  'https://www.fdct.gov.mo/en/other_cooperation_details/article/']
    
    rules = [
        Rule(LinkExtractor(allow=r'\w*\.html'), callback='parse_item')
    ]
    
    def parse_item(self, response):
        coop = CoopItem()

        coop['url'] = response.url
        target = response.css('.acticle-div span ::text').extract()
        coop['title'] = target[0]
        coop['date'] = target[1]
        coop['article'] = response.xpath('//div[@class="acticle-div"]/div[@class="details_body"]//span//text()').extract()

        yield coop
