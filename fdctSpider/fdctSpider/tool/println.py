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