# -*- coding: utf-8 -*-

# Scrapy settings for mysql project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'mysql'

SPIDER_MODULES = ['mysql.spiders']
NEWSPIDER_MODULE = 'mysql.spiders'


MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = '123456'

DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    'mysql.pipelines.DoubanPipeline': 301,

}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'mysql.middlewares.RotateUserAgentMiddleware': 543,
}
