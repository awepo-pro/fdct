# fdct 

This project aims to fetch useful information from [website](https://www.fdct.gov.mo/zh_tw/index.html)

## run
This project uses scrapy framework, which user-defined programs are built in folder `./fdctSpider/fdctSpider/spiders`, so enter this folder:

```
cd fdctSpider/fdctSpider/
```

then run the programs:

### fetch fund information 
```
scrapy runspider fund.py -o fund.json -t json
```

can only fetch few of them

### fetch bulletin
```
scrapy runspider bulletin.py -o bulletin.json -t json
```

### fetch all the images, videos, pdf
```
scrapy runspider images.py
```

cannot fetch files which names have whitespaces.