# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log

from mysql import settings
from mysql.items import MusicItem, MusicReviewItem, VideoItem, VideoReviewItem


class DoubanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == MusicItem:
            try:
                self.cursor.execute("""select * from music_douban where music_url = %s""", item["music_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update music_douban set music_name = %s,music_alias = %s,music_singer = %s,
                            music_time = %s,music_rating = %s,music_votes = %s,music_tags = %s,music_url = %s
                            where music_url = %s""",
                        (item['music_name'],
                         item['music_alias'],
                         item['music_singer'],
                         item['music_time'],
                         item['music_rating'],
                         item['music_votes'],
                         item['music_tags'],
                         item['music_url'],
                         item['music_url']))
                else:
                    self.cursor.execute(
                        """insert into music_douban(music_name,music_alias,music_singer,music_time,music_rating,
                          music_votes,music_tags,music_url)
                          value (%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (item['music_name'],
                         item['music_alias'],
                         item['music_singer'],
                         item['music_time'],
                         item['music_rating'],
                         item['music_votes'],
                         item['music_tags'],
                         item['music_url']))
                self.connect.commit()
            except Exception as error:
                log(error)
            return item

        elif item.__class__ == MusicReviewItem:
            try:
                self.cursor.execute("""select * from music_review_douban where review_url = %s""", item["review_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update music_review_douban set review_title = %s,review_content = %s,review_author = %s,
                            review_music = %s,review_time = %s,review_url = %s
                            where review_url = %s""",
                        (item['review_title'],
                         item['review_content'],
                         item['review_author'],
                         item['review_music'],
                         item['review_time'],
                         item['review_url'],
                         item['review_url']))
                else:
                    self.cursor.execute(
                        """insert into music_review_douban(review_title,review_content,review_author,review_music,review_time,
                          review_url)
                          value (%s,%s,%s,%s,%s,%s)""",
                        (item['review_title'],
                         item['review_content'],
                         item['review_author'],
                         item['review_music'],
                         item['review_time'],
                         item['review_url']))
                self.connect.commit()
            except Exception as error:
                log(error)
            return item

        elif item.__class__ == VideoItem:
            try:
                self.cursor.execute("""select * from video_douban where video_url = %s""", item["video_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update video_douban set video_name= %s,video_alias= %s,video_actor= %s,video_year= %s,
                          video_time= %s,video_rating= %s,video_votes= %s,video_tags= %s,video_url= %s,
                          video_director= %s,video_type= %s,video_bigtype= %s,video_area= %s,video_language= %s,
                          video_length= %s,video_writer= %s,video_desc= %s,video_episodes= %s where video_url = %s""",
                        (item['video_name'],
                         item['video_alias'],
                         item['video_actor'],
                         item['video_year'],
                         item['video_time'],
                         item['video_rating'],
                         item['video_votes'],
                         item['video_tags'],
                         item['video_url'],
                         item['video_director'],
                         item['video_type'],
                         item['video_bigtype'],
                         item['video_area'],
                         item['video_language'],
                         item['video_length'],
                         item['video_writer'],
                         item['video_desc'],
                         item['video_episodes'],
                         item['video_url']))
                else:
                    self.cursor.execute(
                        """insert into video_douban(video_name,video_alias,video_actor,video_year,video_time,
                          video_rating,video_votes,video_tags,video_url,video_director,video_type,video_bigtype,
                          video_area,video_language,video_length,video_writer,video_desc,video_episodes)
                          value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (item['video_name'],
                         item['video_alias'],
                         item['video_actor'],
                         item['video_year'],
                         item['video_time'],
                         item['video_rating'],
                         item['video_votes'],
                         item['video_tags'],
                         item['video_url'],
                         item['video_director'],
                         item['video_type'],
                         item['video_bigtype'],
                         item['video_area'],
                         item['video_language'],
                         item['video_length'],
                         item['video_writer'],
                         item['video_desc'],
                         item['video_episodes']))
                self.connect.commit()
            except Exception as error:
                log(error)
            return item

        elif item.__class__ == VideoReviewItem:
            try:
                self.cursor.execute("""select * from video_review_douban where review_url = %s""", item["review_url"])
                ret = self.cursor.fetchone()
                if ret:
                    self.cursor.execute(
                        """update video_review_douban set review_title = %s,review_content = %s,review_author = %s,
                            review_video = %s,review_time = %s,review_url = %s
                            where review_url = %s""",
                        (item['review_title'],
                         item['review_content'],
                         item['review_author'],
                         item['review_video'],
                         item['review_time'],
                         item['review_url'],
                         item['review_url']))
                else:
                    self.cursor.execute(
                        """insert into video_review_douban(review_title,review_content,review_author,review_video,review_time,
                          review_url)
                          value (%s,%s,%s,%s,%s,%s)""",
                        (item['review_title'],
                         item['review_content'],
                         item['review_author'],
                         item['review_video'],
                         item['review_time'],
                         item['review_url']))
                self.connect.commit()
            except Exception as error:
                log(error)
            return item
        else:
            pass
