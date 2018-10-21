# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboUserItem(scrapy.Item):
    """用户的item"""
    id = scrapy.Field()
    screen_name = scrapy.Field()
    gender = scrapy.Field()
    profile_image_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified = scrapy.Field()
    verified_type = scrapy.Field()
    verified_type_ext = scrapy.Field()
    verified_reason = scrapy.Field()
    close_blue_v = scrapy.Field()
    description = scrapy.Field()
    follow_count = scrapy.Field()
    followers_count = scrapy.Field()
    cover_image_phone = scrapy.Field()
    avatar_hd = scrapy.Field()
    create_time = scrapy.Field()


class UserFollowerItem(scrapy.Item):
    """粉丝 关注 和用户关系表"""

    collections = 'weibo'

    id = scrapy.Field()
    follower = scrapy.Field()


class UserFansItem(scrapy.Item):
    """粉丝 关注 和用户关系表"""

    collections = 'weibo'

    id = scrapy.Field()
    fans = scrapy.Field()


