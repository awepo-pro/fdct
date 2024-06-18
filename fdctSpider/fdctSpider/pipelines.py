from string import whitespace
from .tool.println import println
from urllib.parse import unquote
from typing import Literal
import os

class FdctspiderPipeline:
    
    @staticmethod
    def __check_and_remove_whitespace(strs: list[str]) -> tuple[list[str], bool]:
        """
        check whether the list of strings is empty or not,
        if it is empty, return the original list of strings and False,
        otherwise, remove the whitespace and return the new list of strings and True
        """
        
        if not strs:
            return strs, False
        
        for str in strs:
            ret: list = []

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

    @staticmethod
    def __extract_lang(url: str) -> Literal['zh', 'pt', 'en']:
        """
        return the language used in the article
        """
        
        ret = ''

        if r'/zh_tw/' in url:
            ret = 'zh'
        elif r'/pt/' in url:
            ret = 'pt'
        else:
            ret = 'en'

        return ret

    @staticmethod
    def __extract_title(content: str|list[str], replace: str):
        """
        if no explicit title is found in the article, 
        return the first line of the article as the title
        """
        
        if isinstance(content, list):
            content = content[0]
        content = content.strip()

        return replace if not content else content

    # @staticmethod
    # def __extract_answer(contents):
    #     ret = []
    #     for content in contents:
    #         # if using r'\n', it means check a string '\n' instead of escape character
    #         if '\n' in content:
    #             ret[-1] = ret[-1] + content[2:]
    #         else:
    #             ret.append(content)

    #     return ret
    
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

    # @staticmethod
    # def __QA_format(prizes, question, answer):
    #     arr = []
    #     tmp = []
    #     cnt = 0
        
    #     for q, a in zip(question, answer):
            
    #         if q.startswith('1.'):
    #             if cnt != 0:
    #                 arr.append({'prize': prizes[cnt], 'QA':tmp})
    #                 tmp = []
    #             cnt += 1
                
    #         tmp.append({'Q':q, 'A':a})
        
    #     arr.append({'prize': prizes[-1], 'QA':tmp})
        
    #     return arr
    
    def process_item(self, item, spider):
        article, ok = FdctspiderPipeline.__check_and_remove_whitespace(item['article'])
        if not ok:
            return None
        
        item['article'] = article
        item['title'] = FdctspiderPipeline.__extract_title(item['title'], article[0])
        item['lang'] = FdctspiderPipeline.__extract_lang(item['url'])

        return item

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