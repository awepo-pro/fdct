import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import DownloadItem
from ..tool.println import println

class ImagesPySpider(CrawlSpider):
    name = "download"

    def start_requests(self):
        start_urls = ['https://www.fdct.gov.mo/images', 'https://www.fdct.gov.mo/download/DSS/', 'https://www.fdct.gov.mo/download/OSCOR/', 'https://www.fdct.gov.mo/download/aboutus/', 
                      'https://www.fdct.gov.mo/download/city/', 'https://www.fdct.gov.mo/download/city/urbanfunding/', 'https://www.fdct.gov.mo/download/city/urbanplan/', 
                      'https://www.fdct.gov.mo/download/Performance%20Pledge/', 'https://www.fdct.gov.mo/download/cooperation/', 'https://www.fdct.gov.mo/download/cooperation/SKL/', 
                      'https://www.fdct.gov.mo/download/fund-information/', 'https://www.fdct.gov.mo/download/information/', 'https://www.fdct.gov.mo/download/information/Approved/', 
                      'https://www.fdct.gov.mo/download/information/ClosedFile/', 'https://www.fdct.gov.mo/download/information/SAF_news/', 
                      'https://www.fdct.gov.mo/download/information/SAF_news/20200611/', 'https://www.fdct.gov.mo/download/information/communiqu/', 
                      'https://www.fdct.gov.mo/download/information/communiqu/government-pt/', 'https://www.fdct.gov.mo/download/information/communiqu/government/', 
                      'https://www.fdct.gov.mo/download/information/communiqu/statistical/', 'https://www.fdct.gov.mo/download/information/fund-information/', 
                      'https://www.fdct.gov.mo/download/information/scientific/', 'https://www.fdct.gov.mo/download/popular-science-activities/', 
                      'https://www.fdct.gov.mo/download/popular-science-activities/potential-expansion/', 'https://www.fdct.gov.mo/download/science-and-technology-awards/', 
                      'https://www.fdct.gov.mo/download/subsidy-p/patent/', 'https://www.fdct.gov.mo/download/subsidy-p/polular/', 'https://www.fdct.gov.mo/download/subsidy-p/research/', 
                      'https://www.fdct.gov.mo/download/subsidy/ASC/', 'https://www.fdct.gov.mo/download/subsidy/General/', 'https://www.fdct.gov.mo/download/subsidy/ITP/', 
                      'https://www.fdct.gov.mo/download/subsidy/IURM/', 'https://www.fdct.gov.mo/download/subsidy/IURM/2024/', 'https://www.fdct.gov.mo/download/subsidy/KeyRDPrograms/', 
                      'https://www.fdct.gov.mo/download/subsidy/Macao-project/', 'https://www.fdct.gov.mo/download/subsidy/QandA/', 'https://www.fdct.gov.mo/download/subsidy/RIABC/', 
                      'https://www.fdct.gov.mo/download/subsidy/RIABC/2024/', 'https://www.fdct.gov.mo/download/subsidy/SKL/2023/', 'https://www.fdct.gov.mo/download/subsidy/TRL/', 
                      'https://www.fdct.gov.mo/download/subsidy/agreed_upon_procedure/', 'https://www.fdct.gov.mo/download/subsidy/enterprise/', 
                      'https://www.fdct.gov.mo/download/subsidy/enterprise/2023/', 'https://www.fdct.gov.mo/download/subsidy/enterprise/2024/', 
                      'https://www.fdct.gov.mo/download/subsidy/equip/', 'https://www.fdct.gov.mo/download/subsidy/instrumenttation/', 
                      'https://www.fdct.gov.mo/download/subsidy/lab_RD_centres/', 'https://www.fdct.gov.mo/download/subsidy/lab_RD_centres/', 
                      'https://www.fdct.gov.mo/download/subsidy/overseas_research_for_young/', 'https://www.fdct.gov.mo/download/subsidy/patent/', 
                      'https://www.fdct.gov.mo/download/subsidy/promotion/association/', 'https://www.fdct.gov.mo/download/subsidy/promotion/disaster/', 
                      'https://www.fdct.gov.mo/download/subsidy/promotion/school/', 'https://www.fdct.gov.mo/download/subsidy/research/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/FCT/2019/', 'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2019/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2019/', 'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2020/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2021/', 'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2022/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/GDST/2023/', 'https://www.fdct.gov.mo/download/subsidy/unite/fund/2018/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/fund/2021/', 'https://www.fdct.gov.mo/download/subsidy/unite/fund/2022/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/fund/2023/', 'https://www.fdct.gov.mo/download/subsidy/unite/fund/general/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/fund/old_file/', 'https://www.fdct.gov.mo/download/subsidy/unite/fund/result/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/horizon/2016/', 'https://www.fdct.gov.mo/download/subsidy/unite/horizon/general/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/horizon/old_file/', 'https://www.fdct.gov.mo/download/subsidy/unite/science/2017/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/science/2019/', 'https://www.fdct.gov.mo/download/subsidy/unite/science/2020/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/science/2021/', 'https://www.fdct.gov.mo/download/subsidy/unite/science/2022/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/science/2023/', 'https://www.fdct.gov.mo/download/subsidy/unite/science/2024/', 
                      'https://www.fdct.gov.mo/download/subsidy/unite/science/general/', 'https://www.fdct.gov.mo/download/subsidy/unite/science/old_file/', 
                      'https://www.fdct.gov.mo/download/technological-awards/Macao/', 'https://www.fdct.gov.mo/download/technological-awards/country/2018/', 
                      'https://www.fdct.gov.mo/download/technological-awards/country/2019/', 'https://www.fdct.gov.mo/download/technological-awards/country/2020/', 
                      'https://www.fdct.gov.mo/download/technological-awards/country/2023/', 'https://www.fdct.gov.mo/download/technological-awards/country/general/', 
                      'https://www.fdct.gov.mo/download/technological-awards/guanghua/', 'https://www.fdct.gov.mo/download/technological-awards/hlhl/', 'https://www.fdct.gov.mo/download/wind/']        
        return [scrapy.Request(url=url, callback=self.parse_item) for url in start_urls]
    
    def __is_files(self, links, response):
        path = []
        desired_format = ['.jpg', '.jpeg', '.png', '.mp3', '.mp4', '.pdf', '.ppsx', '.webp', '.docx', '.doc', '.ppt']

        for link in links:
            if link.endswith('/'):
                continue 
            
            for suffix in desired_format:
                if link.endswith(suffix):
                    path.append(response.urljoin(link))
                    break

        return path

    def parse_item(self, response):
        file = DownloadItem()
        println(response.url, 'warning')

        Links = response.xpath('//table//a//@href').extract()
        # println(self.__is_files(Links, response), 'fail', 'debug')
        file['file_urls'] = self.__is_files(Links, response)

        yield file