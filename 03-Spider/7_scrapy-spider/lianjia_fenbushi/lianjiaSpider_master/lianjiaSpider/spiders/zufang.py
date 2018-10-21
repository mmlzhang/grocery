import re

import scrapy

from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.settings import MAX_PAGE
from lianjiaSpider.items import MasterRedisItem


class LianJiaSpider(RedisSpider):
    """爬取链家的 信息"""
    name = 'zufang'

    # 允许访问的域名，爬取的域名
    # allowed_domains = ['lianjia.com']

    """
    北京(bj) 上海(sh) 深圳(sz) 成都(cd) 重庆(cq) 长沙(cs) 大连(dl) 德阳(dy) 广州(gz) 杭州(hz)
    海口(hk) 合肥(hf) 济南(jn) 昆明(km) 南京(nj) 青岛(qd) 苏州(sz) 石家庄(sjz) 沈阳(sy) 天津(tj)
    太原(ty) 武汉(wh) 厦门(xm) 西安(xa) 郑州(zz)
    """
    # 24 个 目标 城市
    cities = [
        'bj', 'sh', 'sz', 'cd', 'cq', 'cs', 'dl', 'dy', 'gz',
        'hz', 'hk', 'hf', 'jn', 'km', 'nj', 'qd', 'sz', 'sjz',
        'sy', 'tj', 'ty', 'wh', 'xm', 'xa', 'zz',
    ]

    # 测试城市
    # cities = ['cd']

   # 租房
    zufang_url = 'https://{city}.lianjia.com/zufang/'

    def start_requests(self):
        for city in self.cities:
            # # 租房
            yield scrapy.Request(self.zufang_url.format(city=city),
                                 callback=self.parse_area)

    def parse_area(self, response):
        """添加不同的区域进行爬取数据"""
        base_url = response.url
        sel = scrapy.Selector(response)

        # 存入Redis 数据库
        item = MasterRedisItem()
        # 添加 redis key  区分不同的爬虫
        item['redis_key'] = 'lianjia:ershoufang'

        areas_urls = sel.xpath('//div[@class="option-list"]/a/@href').extract()
        for area_url in areas_urls:
            area_url = area_url.replace('/zufang/', '')
            url = base_url + area_url
            # 添加页码
            for page in range(1, MAX_PAGE + 1):
                url += re.sub('pg\d+/','pg%s' % page, url)
                item['url'] = url
                yield item

