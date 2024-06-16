# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from string import whitespace
from turtle import fd
from .items import DownloadItem, FundItem, BulletinItem, ImageItem, QAAwardItem, QAFundingItem, DownloadItem, ContactItem
import os
from urllib.request import urlretrieve
from re import match

from urllib.parse import unquote

class FdctspiderPipeline:
    def __init__(self):
        self.image_path = os.getcwd() + '/images/'
        self.file_path = os.getcwd() + '/download/'
        
    @staticmethod
    def __is_empty(str):
        if all(ch in ['\xa0', ' '] for ch in str):
            return True
        return False

    @staticmethod
    def __remove_whitespace(strs):
        ret = []

        for str in strs:
            str = str.replace('\xa0', '')

            for punc in whitespace:
                if punc == ' ':
                    continue
                str = str.replace(punc, '').strip()

            if str:
                ret.append(str)

        return ret

    def __download_image_path(self, paths):
        paths = unquote(paths)
        paths = self.image_path + paths[24:]
        dir_path = os.path.dirname(paths)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return paths
    
    def __download_file_path(self, paths):
        paths = unquote(paths)
        paths = self.file_path + paths[24:]     # path[24:] remove 'https://www.fdct.gov.mo/'
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
    def __extract_title(content, replace):
        content = content[0].strip()

        if not content:
            return replace
        return content[0]

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
    
    # @staticmethod
    # def __extract_answer2(contents):
    #     ret = []
    #     print(contents)
    #     for content in contents:
    #         if match(r'\d*\.', content):
    #             ret.append(content)
    #         else:
    #             ret[-1] = ret[-1] + content
            
        # return ret

    @staticmethod
    def __QA_format(question, answer):
        arr = []
        for q, a in zip(question, answer):
            arr.append({'Q':q, 'A':a})

        return arr
    
    @staticmethod
    def __remove_wrong_path(path):
        ok = True 
        if 'index.html' in path:
            ok = False
        return path, ok
    
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
            bulletin['title'] = FdctspiderPipeline.__extract_title(bulletin['title'], bulletin['article'][0])
            bulletin['lang'] = FdctspiderPipeline.__extract_lang(bulletin['url'])

            return bulletin

        elif isinstance(item, ImageItem):
            images = item

            # store in local directory
            for p in images['path']:
                download_path, ok = FdctspiderPipeline.__remove_wrong_path(p)
                if not ok:
                    continue 
                
                download_path = self.__download_image_path(p)
                urlretrieve(p, download_path)

            return images
        
        elif isinstance(item, DownloadItem):
            download = item

            # store in local directory
            for p in download['path']:
                download_path, ok = FdctspiderPipeline.__remove_wrong_path(p)
                if not ok:
                    continue 
                
                download_path = self.__download_file_path(p)
                urlretrieve(p, download_path)

            return download

        elif isinstance(item, QAAwardItem):
            qa = item 

            qa['answer'] = FdctspiderPipeline.__extract_answer(qa['answer'])
            qa['answer'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['answer']])
            qa['question'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['question']])
            qa['QA'] = FdctspiderPipeline.__QA_format(qa['question'], qa['answer'])
            qa['lang'] = FdctspiderPipeline.__extract_lang(qa['url'])

            return qa
        
        # elif isinstance(item, QAFundingItem):
        #     qa = item 
           
        #     qa['answer'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['answer']]) 
        #     qa['answer'] = FdctspiderPipeline.__extract_answer2(qa['answer'])
        #     qa['question'] = FdctspiderPipeline.__remove_whitespace([str for str in qa['question']])
        #     qa['QA'] = FdctspiderPipeline.__QA_format(qa['question'], qa['answer'])
        #     qa['title'] = FdctspiderPipeline.__extract_title(qa['title'])
        #     qa['lang'] = FdctspiderPipeline.__extract_lang(qa['url']) 

        #     return qa
        
        elif isinstance(item, ContactItem):
            contact = item

            contact['article'] = FdctspiderPipeline.__remove_whitespace([str for str in contact['article']])
            contact['lang'] = FdctspiderPipeline.__extract_lang(contact['url'])
            contact['title'] = FdctspiderPipeline.__extract_title(contact['title'], contact['article'][0])

            return contact