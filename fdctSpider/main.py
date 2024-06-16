import argparse
import os

def update_file(file_paths):
    for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

def main():
    if arg.download:
        print('start downloading all files......')
        print('it will take a long time, be patient......')
        os.system('scrapy crawl images.py 2>> log/files.txt')
        os.system('scrapy crawl images2.py 2>> log/files.txt')
        os.system('scrapy crawl download.py 2>> log/files.txt')
        os.system('scrapy crawl download2.py 2>> log/files.txt')
        
    elif arg.info:
        paths = ['./info/fund.json', './info/contact_us.json', './info/bulletin.json']
        update_file(paths)
        
        print('start fetching information about funding ......')
        os.system('scrapy crawl fund.py -o ./info/fund.json -t json 2>> log/info.txt')
        print('start fetching information about bulletin ......')
        os.system('scrapy crawl bulletin.py -o ./info/bulletin.json -t json 2>> log/info.txt')
        print('start fetching information about contact us ......')
        os.system('scrapy crawl contact_us.py -o ./info/contact_us.json -t json 2>> log/a.txt')
        
    elif arg.qa:
        print('start fetch information about Q&A......')
        paths = ['./info/qa_funding.json', './info/qa_award.json']
        update_file(paths)
        
        # os.system('scrapy crawl QA_funding.py -o ' + paths[0] + ' -t json 2>> log/qa.txt')
        os.system('scrapy crawl QA_award.py -o ' + paths[1] + ' -t json 2>> log/qa.txt')
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--download', nargs='?', const=True, default=False)
    parser.add_argument('--info', nargs='?', const=True, default=False)
    parser.add_argument('--qa', nargs='?', const=True, default=False)
    arg = parser.parse_args()
    
    main()