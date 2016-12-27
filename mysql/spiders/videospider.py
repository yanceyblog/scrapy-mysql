# coding:utf-8

from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mysql.items import VideoItem, VideoReviewItem
from scrapy import log

import re

AREA = re.compile(r"制片国家/地区:</span> (.+?)<br>")
ALIAS = re.compile(r"又名:</span> (.+?)<br>")
LANGUAGE = re.compile(r"语言:</span> (.+?)<br>")
EPISODES = re.compile(r"集数:</span> (.+?)<br>")
LENGTH = re.compile(r"单集片长:</span> (.+?)<br>")


class VideoSpider(CrawlSpider):
    name = 'video'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/tag/',
                  'https://movie.douban.com/tag/?view=cloud'
                  ]
    rules = (Rule(LinkExtractor(allow=r"/tag/((\d+)|([\u4e00-\u9fa5]+)|(\w+))$")),
             Rule(LinkExtractor(allow=r"/tag/((\d+)|([\u4e00-\u9fa5]+)|(\w+))\?start=\d+\&type=T$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/reviews$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/reviews\?start=\d+$")),
             Rule(LinkExtractor(allow=r"/subject/\d+/$"), callback="parse_video", follow=True),
             Rule(LinkExtractor(allow=r"/review/\d+/$"), callback="parse_review", follow=True),
             )

    def parse_video(self, response):
        item = VideoItem()
        try:
            item["video_url"] = response.url
            item["video_name"] = ''.join(
                response.xpath('//*[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract())
            try:
                item["video_year"] = ''.join(
                    response.xpath('//*[@id="content"]/h1/span[@class="year"]/text()').extract()).replace(
                    "(", "").replace(")", "")
            except Exception as e:
                print('Exception:', e)
                item['video_year'] = ''

            introduction = response.xpath('//*[@id="link-report"]/span[@property="v:summary"]/text()').extract()
            if introduction:
                item["video_desc"] = ''.join(introduction).strip().replace("\r\n", " ")
            else:
                item["video_desc"] = ''.join(
                    response.xpath('//*[@id="link-report"]/span/text()').extract()).strip().replace("\r\n", " ")

            item["video_director"] = "|".join(
                response.xpath('//*[@id="info"]/span/span/a[@rel="v:directedBy"]/text()').extract())
            item["video_writer"] = "|".join(
                response.xpath('//*[@id="info"]/span[2]/span[2]/a/text()').extract())

            item["video_actor"] = "|".join(response.xpath("//a[@rel='v:starring']/text()").extract())

            item["video_type"] = "|".join(response.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract())

            S = "".join(response.xpath("//div[@id='info']").extract())
            M = AREA.search(S)
            if M is not None:
                item["video_area"] = "|".join([area.strip() for area in M.group(1).split("/")])
            else:
                item['video_area'] = ''

            A = "".join(response.xpath("//div[@id='info']").extract())
            AL = ALIAS.search(A)
            if AL is not None:
                item["video_alias"] = "|".join([alias.strip() for alias in AL.group(1).split("/")])
            else:
                item["video_alias"] = ""

            video_info = "".join(response.xpath("//div[@id='info']").extract())
            language = LANGUAGE.search(video_info)
            episodes = EPISODES.search(video_info)
            length = LENGTH.search(video_info)

            if language is not None:
                item["video_language"] = "|".join([language.strip() for language in language.group(1).split("/")])
            else:
                item['video_language'] = ''
            if length is not None:
                item["video_length"] = "|".join([runtime.strip() for runtime in length.group(1).split("/")])
            else:
                item["video_length"] = "".join(
                    response.xpath('//*[@id="info"]/span[@property="v:runtime"]/text()').extract())

            item['video_time'] = "/".join(
                response.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract())
            if episodes is not None:
                item['video_bigtype'] = "电视剧"
                item["video_episodes"] = "|".join([episodes.strip() for episodes in episodes.group(1).split("/")])
            else:
                item['video_bigtype'] = "电影"
                item['video_episodes'] = ''
            item['video_tags'] = "|".join(
                response.xpath('//*[@class="tags"]/div[@class="tags-body"]/a/text()').extract())

            try:
                item['video_rating'] = "".join(response.xpath(
                    '//*[@class="rating_self clearfix"]/strong/text()').extract())
                item['video_votes'] = "".join(response.xpath(
                    '//*[@class="rating_self clearfix"]/div/div[@class="rating_sum"]/a/span/text()').extract())
            except Exception as error:
                item['video_rating'] = '0'
                item['video_votes'] = '0'
                log(error)

            yield item
        except Exception as error:
            log(error)

    def parse_review(self, response):
        try:
            item = VideoReviewItem()
            item['review_title'] = "".join(response.xpath('//*[@property="v:summary"]/text()').extract())
            content = "".join(
                response.xpath('//*[@id="link-report"]/div[@property="v:description"]/text()').extract())
            item['review_content'] = content.lstrip().rstrip().replace("\n", " ")
            item['review_author'] = "".join(response.xpath('//*[@property = "v:reviewer"]/text()').extract())
            item['review_video'] = "".join(response.xpath('//*[@class="main-hd"]/a[2]/text()').extract())
            item['review_time'] = "".join(response.xpath('//*[@class="main-hd"]/p/text()').extract())
            item['review_url'] = response.url
            yield item
        except Exception as error:
            log(error)
