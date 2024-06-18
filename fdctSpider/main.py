import argparse
import os
from fdctSpider.tool.println import println

def update_file(file_paths: list[str]) -> None:
    for file_path in file_paths:
        if os.path.exists(file_path):
            println('files existed, removing ' + os.path.basename(file_path), 'warning')
            os.remove(file_path)
                
def check_file(dirs: list[str]) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            println('file doesn\'t exist, creating ' + dir, 'warning')
            os.makedirs(dir)

def main():
    if arg.download:
        println('it will take a long time, be patient......')
        println('start downloading all files')
        
        os.system('scrapy crawl images -L WARN 2>> log/download.txt')
        
        println('finish downloading all images')
        println('start downloading all other formats')
        
        os.system('scrapy crawl download -L WARN 2>> log/download.txt')
        println('finish 2/3, be patient')
        
        os.system('scrapy crawl files -L WARN 2>> log/download.txt')
        
    elif arg.info:
        output_paths = ['./info/fund.json', './info/bulletin.json', './info/bulletin_detail.json', './info/contact_us.json', 
                        './info/transformation_case.json', './info/mainland_coop.json', './info/other_coop.json', 
                        './info/expert_database.json']
        update_file(output_paths)
        check_file(['log/'])
        
        println('start fetching information about funding')
        os.system('scrapy crawl fund -o ' + output_paths[0] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about bulletin')
        os.system('scrapy crawl bulletin -o ' + output_paths[1] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about bulletin detail')
        os.system('scrapy crawl bulletin_detail -o ' + output_paths[2] + ' -t json -L WARN 2>> log/info.txt')

        println('start fetching information about contact us')
        os.system('scrapy crawl contact_us -o ' + output_paths[3] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about transformation case')
        os.system('scrapy crawl transformation_case -o ' + output_paths[4] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about mainland-macau cooperation')
        os.system('scrapy crawl mainland_coop -o ' + output_paths[5] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about other country and macau cooperation')
        os.system('scrapy crawl other_coop -o ' + output_paths[6] + ' -t json -L WARN 2>> log/info.txt')
        
        println('start fetching information about experct database')
        os.system('scrapy crawl expert_database -o ' + output_paths[7] + ' -t json -L WARN 2>> log/info.txt')
        
    # elif arg.qa:
    #     println('checking if the files exist......')
    #     paths = ['./info/qa_funding.json', './info/qa_award.json']
    #     update_file(paths)
        
    #     println('start fetch information about Q&A......')
    #     # os.system('scrapy crawl QA_funding.py -o ' + paths[0] + ' -t json 2>> log/qa.txt')
    #     os.system('scrapy crawl QA_award.py -o ' + paths[1] + ' -t json 2>> log/qa.txt')
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--download', nargs='?', const=True, default=False)
    parser.add_argument('--info', nargs='?', const=True, default=False)
    # parser.add_argument('--qa', nargs='?', const=True, default=False)
    arg = parser.parse_args()
    
    main()