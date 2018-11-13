# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import pymysql
import redis
from scrapy.conf import settings


class LianjiaspiderPipeline(object):
    def process_item(self, item, spider):
        # 添加时间
        item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%m')
        return item


class LianjiaMongo(object):

    # def __init__(self):
    #
    #     conn = pymongo.MongoClient(host=settings['MONGO_HOST'],
    #                                port=settings['MONGO_PORT'])
    #     # self.database = conn.lianjia
    #     self.database = conn.test

    def process_item(self, item, spider):
        conn = pymysql.connect(host='localhost', port=3306, user='lanms', passwd='123456', db='test', charset='utf8',
                               autocommit=False)
        data = dict(item)
        keys = ",".join(list(data.keys()))[:15]
        values = ",".join(list(data.values()))[:15]
        name = spider.name

        try:
            with conn.cursor() as cursor:
                result = cursor.execute('insert into test (v1, v2, v3) values (%s, %s, %s)', (name, keys, values))
            conn.commit()
        finally:
            conn.close()
        # try:
        #     # 表名  拼接 city 和 类型  二手房 成交 租房 新房
        #     # collection = self.database[item['city'] + '_' + item['type']]
        #     collection = self.database['test']
        #     collection.update(
        #         {'house_code': item['house_code']},
        #         {'$set': dict(item)},
        #         upsert=True
        #     )
        # except:
        #     pass
        return item


class LianjiaReids(object):

    def __init__(self):
        redis.Redis(host=settings['REDIS_HOST'],
                    port=settings['REDIS_PORT'])