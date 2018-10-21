# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime

import pymongo
from scrapy.conf import settings

from weiboSpider.items import WeiboUserItem, UserFollowerItem, UserFansItem


class UserCreateTimePipeline(object):
    """添加创建时间"""

    def process_item(self, item, spider):
        if isinstance(item, WeiboUserItem):
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        return item


# class WeibospiderPipeline(object):
#
#     def process_item(self, item, spider):
#         return item


class WeiboPymongoPipeline(object):
    """保存数据到 mongodb"""

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
                                   port=settings['MONGO_PORT'])
        db = conn[settings['MONGO_DATABASE']]
        self.collection = db[settings['MONGO_COLLECTION']]

    def process_item(self, item, spider):

        # 判断是保存用户还是 添加粉丝和 关注 关系
        if isinstance(item, WeiboUserItem):
            self.collection.update({'id': item['id']}, {'$set': dict(item)}, upsert=True)
        # 插入关注
        if isinstance(item, UserFollowerItem):
            self.collection.update(
                {'id': item['id']},
                {'$addToSet': {
                    'follower': {'$each': item['follower']}
                }},
                True
            )
        # 插入粉丝
        if isinstance(item, UserFansItem):
            self.collection.update(
                {'id': item['id']},
                {'$addToSet': {
                    'fans': {'$each': item['fans']}
                }},
                True
            )

        return item
