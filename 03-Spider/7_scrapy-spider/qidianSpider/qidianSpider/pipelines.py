# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 管道， 持久化, 存储数据库


import pymongo
from scrapy.conf import settings


class DoubanspiderPipeline(object):

    def __init__(self):
        conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
                                   port=settings['MONGO_PORT'],)
        db = conn[settings['MONGO_DB']]
        self.collection = db[settings['MONGO_COLLECTION']]

    def process_item(self, item, spider):

        for i in range(len(item['movie_name'])):
            data = {}
            data['movie_name'] = item['movie_name'][i]
            data['img'] = item['img'][i]
            data['director'] = item['director'][i]
            data['year'] = item['year'][i]
            data['country'] = item['country'][i]
            data['type'] = item['type'][i]
            data['rate'] = item['rate'][i]
            # 插入数据库
            self.collection.insert(data)

        return item
