# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'SUB=_2A25x8MsdDeRhGeFP6VcY8ijKyT-IHXVTGtVVrDV6PUJbktAKLWXVkW1NQTn9I6J_GgryM47nqYF2vvaP-gmbebJD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFTsNj.VT6GKdXpjG4CpJb05JpX5KzhUgL.FoMpeo-4eoqceoe2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeKzf1KzcSoz0; SUHB=04WuS7Oag8hWi0; SSOLoginState=1559542605; MLOGIN=1; _T_WM=11342552435; M_WEIBOCN_PARAMS=luicode%3D20000174'
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'
