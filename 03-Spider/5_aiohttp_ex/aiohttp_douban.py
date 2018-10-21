
"""

爬取豆瓣的电影信息， 并且将其存储在 mongodb  的数据库中

"""

import json
import aiohttp
import asyncio
import pymongo


class DoubanMovie():

    def __init__(self):
        """
        初始化
        @:param self.movie_url  每个 tag 下 当前页的电影的URL
        @:param self.tag_ulr    所有的 标签的 URL 可以获得多有的电影 分类 标签
        @:param self.mongo   mongodb 的 连接
        """
        super(DoubanMovie, self).__init__()
        self.movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%s&sort=recommend&page_limit=20&page_start=%s'
        self.tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
        self.mongo = pymongo.MongoClient('mongodb://127.0.0.1:27107')

    async def get_html(self):
        """获取信息"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.tag_url) as response:
                tags = await self.parse(await response.text())
                self.tags = tags['tags']

                for tag in self.tags:
                    for page_num in range(1, 10):
                        async with session.get(self.movie_url % (tag, page_num * 20)) as response:
                            data = await self.parse(await response.text())
                            print(data)
                            for movie_info in data['subjects']:
                                self.insert_data(movie_info)  # 保存到 mongodb 中

    async def parse(self, response):
        """解码 json 格式的响应"""
        tag_json = json.loads(response)
        return tag_json

    async def insert_data(self, data):
        """将获得的数据存储到 mongodb 的数据库中"""
        database = self.mongo['spider']
        collection = database['douban']
        await collection.insert_one(data)

    def run(self):
        """ 执行函数， 将任务放在 任务列表中 异步执行"""
        loop = asyncio.get_event_loop()
        task = asyncio.wait([self.get_html()])
        loop.run_until_complete(task)  # 执行函数
        loop.close()


def main():

    douban = DoubanMovie()
    douban.run()


if __name__ == '__main__':
    main()