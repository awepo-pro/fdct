# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FundItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    date = scrapy.Field()
    lang = scrapy.Field()

class BulletinItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    lang = scrapy.Field()

class ImageItem(scrapy.Item):
    path = scrapy.Field()
    name = scrapy.Field()