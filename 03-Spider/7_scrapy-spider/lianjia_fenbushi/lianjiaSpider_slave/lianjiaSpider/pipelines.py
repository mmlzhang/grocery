# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymongo
from scrapy.conf import settings


class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):
        # 添加时间
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
        return item


class LianjiaMongo(object):

    def __init__(self):

        conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
                                   port=settings['MONGO_PORT'])
        # self.database = conn.lianjia
        self.database = conn.test

    def process_item(self, item, spider):
        try:
            # 表名  拼接 city 和 type (二手房 成交 租房 新房)
            collection = self.database[item['city'] + '_' + item['type']]
            # collection = self.database['test']
            collection.update(
                {'house_code': item['house_code']},
                {'$set': dict(item)},
                upsert=True)
        except:
            pass
        return item
