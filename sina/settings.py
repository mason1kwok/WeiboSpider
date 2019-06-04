# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'SUB=_2A25x8a_PDeRhGeFP6VYW9inMwzmIHXVTHTGHrDV6PUJbktANLVSikW1NQTn94Fe6-4rsCbf05-MmUaB76gxp_GbT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWaxXB6lGAdns-KIZFehjh25JpX5KzhUgL.FoMpeoBNSoM71h-2dJLoI02LxK-L1hnLB-zLxKnLB-qLBoBLxK-L1K5L12-LxKqL1-BLBK-LxKBLBonLBo99x-8z; SUHB=0JvgZv2zdHgJl1; SSOLoginState=1559617439; MLOGIN=1; _T_WM=59456585887; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=uicode%3D20000174'
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
MONGO_URI = "mongodb://root:qwer1234@10.100.31.73:27017/storage?authSource=admin"
