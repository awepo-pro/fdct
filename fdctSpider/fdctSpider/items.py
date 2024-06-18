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
    

class BulletinDetailItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    lang = scrapy.Field()


class ImageItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    

class DownloadItem(scrapy.Item):
    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    

class FileItem(scrapy.Item):
    title = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()


class QAAwardItem(scrapy.Item):
    url = scrapy.Field()
    QandA = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    title = scrapy.Field()
    lang = scrapy.Field()
    prizes = scrapy.Field()


class QAFundingItem(scrapy.Item):
    url = scrapy.Field()
    QandA = scrapy.Field()
    question = scrapy.Field()
    answer = scrapy.Field()
    title = scrapy.Field()
    lang = scrapy.Field()


class ContactItem(scrapy.Item):
    url = scrapy.Field()
    article = scrapy.Field()
    lang = scrapy.Field()
    title = scrapy.Field()
    
class TransItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    date = scrapy.Field()
    lang = scrapy.Field()
    
class CoopItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    article = scrapy.Field()
    date = scrapy.Field()
    lang = scrapy.Field()