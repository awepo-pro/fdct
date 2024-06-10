# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from string import whitespace

def remove_whitespace(str):
    for punc in whitespace:
        str = str.replace(punc, '')

    # extra process
    str = str.replace(u'\xa0', u'')

    return str

class FdctspiderPipeline:
    def process_item(self, fund, spider):
        if fund['article'] is not None:
            fund['article'] = ''.join(fund['article'])
            fund['article'] = remove_whitespace(fund['article'])

        fund['title'] = fund['title'].strip() if fund['title'] is not None else ''
        return fund
