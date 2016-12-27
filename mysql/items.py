# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Item, Field


# 音乐
class MusicItem(Item):
    music_name = Field()
    music_alias = Field()
    music_singer = Field()
    music_time = Field()
    music_rating = Field()
    music_votes = Field()
    music_tags = Field()
    music_url = Field()


# 乐评
class MusicReviewItem(Item):
    review_title = Field()
    review_content = Field()
    review_author = Field()
    review_music = Field()
    review_time = Field()
    review_url = Field()


# 视频
class VideoItem(Item):
    video_name = Field()
    video_alias = Field()
    video_actor = Field()
    video_year = Field()
    video_time = Field()
    video_rating = Field()
    video_votes = Field()
    video_tags = Field()
    video_url = Field()
    video_director = Field()
    video_type = Field()
    video_bigtype = Field()
    video_area = Field()
    video_language = Field()
    video_length = Field()
    video_writer = Field()
    video_desc = Field()
    video_episodes = Field()


# 影评
class VideoReviewItem(Item):
    review_title = Field()
    review_content = Field()
    review_author = Field()
    review_video = Field()
    review_time = Field()
    review_url = Field()
