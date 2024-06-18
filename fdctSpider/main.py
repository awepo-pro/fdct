import argparse
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def println(str, status='ok', replace=''):
    content = status 
    if replace != '':
        content = replace 
        
    if status == 'ok':
        print(bcolors.OKGREEN, '[{:^10s}]: '.format(content), str, bcolors.ENDC)
    elif status == 'fail':
        print(bcolors.FAIL, '[{:^10s}]: '.format(content), str, bcolors.ENDC)
    elif status == 'warning':
        print(bcolors.WARNING,'[{:^10s}]: '.format(content), str, bcolors.ENDC)

def update_file(file_paths):
    for file_path in file_paths:
            if os.path.exists(file_path):
                println('files existed, removing ' + os.path.basename(file_path), 'warning')
                os.remove(file_path)

def main():
    if arg.download:
        println('it will take a long time, be patient......')
        println('start downloading all files')
        
        os.system('scrapy crawl images.py 2>> log/files.txt')
        
        println('finish downloading all images')
        println('start downloading all other formats')
        
        os.system('scrapy crawl download.py 2>> log/files.txt')
        println('finish 2/3, be patient')
        
        os.system('scrapy crawl files.py 2>> log/files.txt')
        
    elif arg.info:
        output_paths = ['./info/fund.json', './info/bulletin.json', './info/bulletin_detail.json', './info/contact_us.json', './info/transformation_case.json']
        update_file(output_paths)
        
        println('start fetching information about funding')
        os.system('scrapy crawl fund.py -o ' + output_paths[0] + ' -t json 2>> log/info.txt')
        
        println('start fetching information about bulletin')
        os.system('scrapy crawl bulletin.py -o ' + output_paths[1] + ' -t json 2>> log/info.txt')
        
        println('start fetching information about bulletin detail')
        os.system('scrapy crawl bulletin.py -o ' + output_paths[2] + ' -t json 2>> log/info.txt')

        println('start fetching information about contact us')
        os.system('scrapy crawl contact_us.py -o ' + output_paths[3] + ' -t json 2>> log/info.txt')
        
        println('start fetching information about funding')
        os.system('scrapy crawl transformation_case.py -o ' + output_paths[0] + ' -t json 2>> log/transformation.txt')
        
    elif arg.cooperation:
        output_paths = ['./info/mainland_coop.json', './info/other_coop.json', './info/expert_database.json']
        update_file(output_paths)
        
        println('start fetching information about mainland-macau cooperation')
        os.system('scrapy crawl mainland_coop.py -o ' + output_paths[0] + ' -t json 2>> log/coop.txt')
        
        println('start fetching information about other country and macau cooperation')
        os.system('scrapy crawl other_coop.py -o ' + output_paths[1] + ' -t json 2>> log/coop.txt')
        
        println('start fetching information about experct database')
        os.system('scrapy crawl expert_database.py -o ' + output_paths[2] + ' -t json 2>> log/coop.txt')

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
    parser.add_argument('--cooperation', nargs='?', const=True, default=False)
    parser.add_argument('--trans', nargs='?', const=True, default=False)
    arg = parser.parse_args()
    
    main()