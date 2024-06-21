from pandas import read_json 
from nltk import word_tokenize
from os import listdir, getcwd
from os.path import isfile, join

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
        print(bcolors.OKGREEN, '[{:^11s}]: '.format(content), str, bcolors.ENDC)
    elif status == 'fail':
        print(bcolors.FAIL, '[{:^11s}]: '.format(content), str, bcolors.ENDC)
    elif status == 'warning':
        print(bcolors.WARNING,'[{:^11s}]: '.format(content), str, bcolors.ENDC)

def wc(data: dict[str, dict], lang: dict[int, str]) -> int:
    ret = 0

    for article, lg in zip(data['article'].values(), lang.values()):
        for x in article:
            if lg == 'zh':
                for y in x:
                    t = word_tokenize(y)
                    ret += len(t)
            else:
                t = word_tokenize(x)
                ret += len(t)
        
    for title, lg in zip(data['title'].values(), lang.values()):
        if lg == 'zh':
            for x in title:
                ret += len(word_tokenize(x))
        else:
            ret += len(word_tokenize(title))
        
    if data.get('date') == None:
        return ret
    
    for date in data['date'].values():
        ret += len(word_tokenize(str(date)))

    return ret

if __name__ == '__main__':
    relative_path = '../info/'
    folder_path = join(getcwd(), relative_path)
    files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    tot = 0
    
    for file in files:
        println(file, replace='fetching')
        data = read_json(relative_path + file)
        data_dict = data.to_dict()

        tot += wc(data_dict, data_dict['lang'])
    
    println('total words in article: ' + str(tot))