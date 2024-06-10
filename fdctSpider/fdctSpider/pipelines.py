# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from string import whitespace
from fdctSpider.items import FundItem, BulletinItem, ImageItem
import os
from urllib.request import urlretrieve

class FdctspiderPipeline:
    def __init__(self):
        self.download_path = os.getcwd() + '/images/'

    def __remove_whitespace(self, str):
        for punc in whitespace:
            if punc == ' ':
                continue
            str = str.replace(punc, '')

        # extra process
        str = str.replace(u'\xa0', u'')

        return str

    def __download_path(self, paths):
        paths = self.download_path + paths[25:]
        dir_path = os.path.dirname(paths)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return paths

    def process_item(self, item, spider):
        if isinstance(item, FundItem):
            fund = item
            if fund['article'] is not None:
                fund['article'] = ''.join(fund['article'])
                fund['article'] = self.__remove_whitespace(fund['article'])

            fund['title'] = fund['title'].strip() if fund['title'] is not None else ''

            return fund

        elif isinstance(item, BulletinItem):
            bulletin = item

            bulletin['article'] = ''.join(bulletin['article'])
            bulletin['article'] = self.__remove_whitespace(bulletin['article'])
            bulletin['title'] = bulletin['title'].strip() if bulletin['title'] is not None else ''

            return bulletin

        elif isinstance(item, ImageItem):
            images = item
            names = []

            # store in local directory
            for p in images['path']:
                download_path = self.__download_path(p)
                urlretrieve(p, download_path)
                names.append(download_path)

            images['name'] = names

            return images
