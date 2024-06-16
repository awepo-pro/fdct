# fdct 

This project aims to fetch useful information from [website](https://www.fdct.gov.mo/zh_tw/index.html)

# run
before start running, the program install the packages by

```shell
pip install -r requirement.txt
```

enter folder /fdctSpider/ and run the programming using the following commands

# fetch information
it fetches all the pages' information and stored in /fdctSpider/info/, there are several files to distinguish different structure of the webpages

```shell
python main.py --info
```

# fetch files
it fetches all the files, including png, jpg, jpg, mp4... formats and store them in folder /fdctSpider/images/ and /fdctSpider/download/
However, this process may take for a long time, don't close the terminal when loading.

```shell
python main.py --download
```

# fetch Q&A
there are Q&A in the webpage, so it formats in structure like one question with one answer. fetched data can be found in folder /fdctSpider/info/

```shell
python main.py --qa
```

## NOTE
[this website](https://www.fdct.gov.mo/zh_tw/research_funding1.html) doesn't finish reformat into Q&A. Therefore, there is only 1 webpage suit for this format