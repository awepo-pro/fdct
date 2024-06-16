# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from string import whitespace
from .items import FundItem, BulletinItem, ImageItem, QAAwardItem, QAFundingItem
import os
from urllib.request import urlretrieve

class FdctspiderPipeline:
    def __init__(self):
        self.download_path = os.getcwd() + '/images/'

    @staticmethod
    def __is_empty(str):
        if all(ch in ['\xa0', ' '] for ch in str):
            return True
        return False

    @staticmethod
    def __remove_whitespace(strs):
        ret = []

        for str in strs:
            str = str.replace(u'\xa0', u'')

            for punc in whitespace:
                if punc == ' ':
                    continue
                str = str.replace(punc, '').strip()

            if str:
                ret.append(str)

        return ret

    def __download_path(self, paths):
        paths = self.download_path + paths[25:]
        dir_path = os.path.dirname(paths)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return paths

    @staticmethod
    def __extract_lang(url):
        ret = ''

        if r'/zh_tw/' in url:
            ret = 'zh'
        elif r'/pt/' in url:
            ret = 'pt'
        else:
            ret = 'en'

        return ret

    @staticmethod
    def __extract_title(content):
        content = content[0].strip()

        if not content:
            return content[0]
        return content

    @staticmethod
    def __extract_answer(contents):
        ret = []
        for content in contents:
            # if using r'\n', it means check a string '\n' instead of escape character
            if '\n' in content:
                ret[-1] = ret[-1] + content[2:]
            else:
                ret.append(content)

        return ret

    @staticmethod
    def __QA_format(question, answer):
        arr = []
        for q, a in zip(question, answer):
            arr.append({'Q':q, 'A':a})

        return arr

    def process_item(self, item, spider):
        if isinstance(item, FundItem):
            fund = item

            # if debug, comment it out
            if FdctspiderPipeline.__is_empty([str for str in fund['article']]):
                return None

            fund['article'] = FdctspiderPipeline.__remove_whitespace([str for str in fund['article']])

            fund['title'] = fund['title'].strip() if fund['title'] is not None else ''
            fund['lang'] = FdctspiderPipeline.__extract_lang(fund['url'])

            return fund

        elif isinstance(item, BulletinItem):
            bulletin = item

              # if debug, comment it out
            if FdctspiderPipeline.__is_empty([str for str in bulletin['article']]):
                return None

            bulletin['article'] = FdctspiderPipeline.__remove_whitespace([str for str in bulletin['article']])
            bulletin['title'] = FdctspiderPipeline.__extract_title(bulletin['title'])
            bulletin['lang'] = FdctspiderPipeline.__extract_lang(bulletin['url'])

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

        elif isinstance(item, QAAwardItem):
            qa = item 

            qa['answer'] = FdctspiderPipeline.__extract_answer(qa['answer'])
            qa['answer'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['answer']])
            qa['question'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['question']])
            qa['QA'] = FdctspiderPipeline.__QA_format(qa['question'], qa['answer'])
            qa['title'] = FdctspiderPipeline.__extract_title(qa['title'])
            qa['lang'] = FdctspiderPipeline.__extract_lang(qa['url'])

            return qa
