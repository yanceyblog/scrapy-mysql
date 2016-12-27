# coding:utf-8

from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mysql.items import MusicItem, MusicReviewItem
from scrapy import log

import re


class MusicSpider(CrawlSpider):
    name = 'music'
    allowed_domains = ['music.douban.com']
    start_urls = ['https://music.douban.com/tag/',
                  'https://music.douban.com/tag/?view=cloud'
                  ]
    rules = (Rule(LinkExtractor(allow=r"/tag/((\d+)|([\u4e00-\u9fa5]+)|(\w+))$")),
             Rule(LinkExtractor(allow=r"/tag/((\d+)|([\u4e00-\u9fa5]+)|(\w+))\?start=\d+\&type=T$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?sort=time\&start=\d+$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/$"), callback="parse_music", follow=True),
             Rule(LinkExtractor(allow=r"/review/\d+/$"), callback="parse_review", follow=True),
             )

    def parse_music(self, response):
        item = MusicItem()
        try:
            item['music_name'] = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()[0]
            content = "".join(response.xpath('//*[@id="info"]').extract())
            info = response.xpath('//*[@id="info"]/span').extract()
            item['music_alias'] = ""
            item['music_singer'] = ""
            item['music_time'] = ""
            for i in range(0, len(info)):
                if "又名" in info[i]:
                    if i == 0:
                        item['music_alias'] = response.xpath('//*[@id="info"]/text()').extract()[1] \
                            .replace("\xa0", "").replace("\n", "").rstrip()
                    elif i == 1:
                        item['music_alias'] = response.xpath('//*[@id="info"]/text()').extract()[2] \
                            .replace("\xa0", "").replace("\n", "").rstrip()
                    elif i == 2:
                        item['music_alias'] = response.xpath('//*[@id="info"]/text()').extract()[3] \
                            .replace("\xa0", "").replace("\n", "").rstrip()

                    else:
                        item['music_alias'] = ""
                        # break
                if "表演者" in info[i]:
                    if i == 0:
                        item['music_singer'] = "|".join(
                            response.xpath('//*[@id="info"]/span[1]/span/a/text()').extract())
                    elif i == 1:
                        item['music_singer'] = "|".join(
                            response.xpath('//*[@id="info"]/span[2]/span/a/text()').extract())
                    elif i == 2:
                        item['music_singer'] = "|".join(
                            response.xpath('//*[@id="info"]/span[3]/span/a/text()').extract())
                    else:
                        item['music_singer'] = ""
                        # break
                if "发行时间" in info[i]:
                    nbsp = re.findall(r"<span class=\"pl\">发行时间:</span>(.*?)<br>", content, re.S)
                    item['music_time'] = "".join(nbsp).replace("\xa0", "").replace("\n", "").replace(" ", "")
                    # break
            try:
                item['music_rating'] = "".join(response.xpath(
                    '//*[@class="rating_self clearfix"]/strong/text()').extract())
                item['music_votes'] = "".join(response.xpath(
                    '//*[@class="rating_self clearfix"]/div/div[@class="rating_sum"]/a/span/text()').extract())
            except Exception as error:
                item['music_rating'] = '0'
                item['music_votes'] = '0'
                log(error)
            item['music_tags'] = "|".join(response.xpath('//*[@id="db-tags-section"]/div/a/text()').extract())
            item['music_url'] = response.url
            yield item
        except Exception as error:
            log(error)

    def parse_review(self, response):
        try:
            item = MusicReviewItem()
            item['review_title'] = "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            content = "".join(
                response.xpath('//*[@id="link-report"]/div[@property="v:description"]/text()').extract())
            item['review_content'] = content.lstrip().rstrip().replace("\n", " ")
            item['review_author'] = "".join(response.xpath('//*[@property = "v:reviewer"]/text()').extract())
            item['review_music'] = "".join(response.xpath('//*[@class="main-hd"]/a[2]/text()').extract())
            item['review_time'] = "".join(response.xpath('//*[@class="main-hd"]/p/text()').extract())
            item['review_url'] = response.url
            yield item
        except Exception as error:
            log(error)
