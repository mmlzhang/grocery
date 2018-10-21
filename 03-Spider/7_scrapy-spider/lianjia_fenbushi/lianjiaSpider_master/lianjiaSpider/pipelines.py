# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
from scrapy.conf import settings


class LianjiaRedis(object):

    def __init__(self):
        self.r = redis.Redis(host=settings['REDIS_HOST'],
                    port=settings['REDIS_PORT'])

    def process_item(self, item, spider):
        self.r.lpush(item['redis_key'], item['url'])
        return item
