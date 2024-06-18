# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from string import whitespace
from .items import BulletinDetailItem, DownloadItem, FundItem, BulletinItem, ImageItem, QAAwardItem, QAFundingItem, DownloadItem, ContactItem, BulletinDetailItem, TransItem, CoopItem, FileItem
import os
from urllib.request import urlretrieve
import re
from .tool.println import println

from urllib.parse import unquote

class FdctspiderPipeline:
    def __init__(self):
        self.image_path = os.getcwd() + '/images/'
        self.download_path = os.getcwd() + '/download/'
        self.file_path = os.getcwd() + '/files/'
        
    @staticmethod
    def __check_and_remove_whitespace(strs):
        if not strs:
            return strs, False
        
        for str in strs:
            ret = []

            for str in strs:
                str = str.replace('\xa0', '').replace('\u202d', '').replace('\u202c', '')

                for punc in whitespace:
                    if punc == ' ':
                        continue
                    str = str.replace(punc, '').strip()

                if str:
                    ret.append(str)

        if not ret:
            return strs, False
            
        return ret, True

    def __download_image_path(self, paths):
        paths = unquote(paths)
        paths = self.image_path + paths[24:]
        dir_path = os.path.dirname(paths)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return paths
    
    def __download_download_path(self, paths):
        paths = unquote(paths)
        paths = self.download_path + paths[24:]     # path[24:] remove 'https://www.fdct.gov.mo/'
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
        if isinstance(content, list):
            content = content[0]
        content = content.strip()

        if not content:
            return replace
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
    def __QA_format(prizes, question, answer):
        arr = []
        tmp = []
        cnt = 0
        
        for q, a in zip(question, answer):
            
            if q.startswith('1.'):
                if cnt != 0:
                    arr.append({'prize': prizes[cnt], 'QA':tmp})
                    tmp = []
                cnt += 1
                
            tmp.append({'Q':q, 'A':a})
        
        arr.append({'prize': prizes[-1], 'QA':tmp})
        
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

            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(fund['article'])
            if not ok:
                return None
            
            fund['article'] = article
            fund['title'] = fund['title'].strip() if fund['title'] is not None else ''
            fund['lang'] = FdctspiderPipeline.__extract_lang(fund['url'])

            return fund

        elif isinstance(item, BulletinItem):
            bulletin = item

            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(bulletin['article'])
            if not ok:
                return None
                    
            bulletin['article'] = article
            bulletin['title'] = FdctspiderPipeline.__extract_title(bulletin['title'], article[0])
            bulletin['lang'] = FdctspiderPipeline.__extract_lang(bulletin['url'])

            return bulletin
        
        elif isinstance(item, BulletinDetailItem):
            detail = item
            
            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(detail['article'])
            if not ok:
                return None
            
            detail['article'] = article 
            detail['title'] = FdctspiderPipeline.__extract_title(detail['title'], article[0])
            detail['lang'] = FdctspiderPipeline.__extract_lang(detail['url'])

            return detail
            

        # elif isinstance(item, ImageItem):
        #     images = item

        #     # store in local directory
        #     for p in images['path']:
        #         download_path, ok = FdctspiderPipeline.__remove_wrong_path(p)
        #         if not ok:
        #             continue 
                
        #         download_path = self.__download_image_path(p)
        #         urlretrieve(p, download_path)

        #     return images
        
        # elif isinstance(item, DownloadItem):
        #     download = item

        #     # store in local directory
        #     for p in download['path']:
        #         download_path, ok = FdctspiderPipeline.__remove_wrong_path(p)
        #         if not ok:
        #             continue 
                
        #         download_path = self.__download_download_path(p)
        #         urlretrieve(p, download_path)

        #     return download
        
        # elif isinstance(item, FileItem):
        #     file = item

            # # store in local directory
            # for p in file['path']:
            #     file_path, ok = FdctspiderPipeline.__remove_wrong_path(p)
            #     if not ok:
            #         continue 
                
            #     file_path = self.__download_file_path(p)
            #     urlretrieve(p, file_path)

            # return file

        # elif isinstance(item, QAAwardItem):
        #     qa = item 

        #     qa['answer'] = FdctspiderPipeline.__extract_answer(qa['answer'])
        #     answer, _ = FdctspiderPipeline.__check_and_remove_whitespace(qa['answer'])
        #     question, _ = FdctspiderPipeline.__check_and_remove_whitespace(qa['question'])

        #     qa['QandA'] = FdctspiderPipeline.__QA_format(qa['prizes'], question, answer)
        #     qa['question'] = question
        #     qa['answer'] = answer
        #     qa['lang'] = FdctspiderPipeline.__extract_lang(qa['url'])
        #     qa['title'] = qa['title'][0].strip()

        #     return qa
        
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

            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(contact['article'])
            if not ok:
                return None
            
            contact['lang'] = FdctspiderPipeline.__extract_lang(contact['url'])
            contact['title'] = FdctspiderPipeline.__extract_title(contact['title'], article[0])
            contact['article'] = article

            return contact
        
        elif isinstance(item, TransItem):
            trans = item 
            
            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(trans['article'])
            if not ok:
                return None
            
            trans['lang'] = FdctspiderPipeline.__extract_lang(trans['url'])
            trans['title'] = FdctspiderPipeline.__extract_title(trans['title'], article[0])
            trans['article'] = article
            
            return trans
        
        elif isinstance(item, CoopItem):
            coop = item
            
            article, ok = FdctspiderPipeline.__check_and_remove_whitespace(coop['article'])
            if not ok:
                return None
            
            coop['lang'] = FdctspiderPipeline.__extract_lang(coop['url'])
            coop['title'] = FdctspiderPipeline.__extract_title(coop['title'], article[0])
            coop['article'] = article
            
            return coop
        
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse

class CustomFilePipelines(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        println(request.url, 'ok', 'fetching')
        return os.path.basename(unquote(urlparse(request.url).path))
   
class CustomImagePipelines(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        println(request.url, 'ok', 'fetching')
        return os.path.basename(unquote(urlparse(request.url).path))