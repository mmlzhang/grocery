import re

import scrapy

from lianjiaSpider.items import LianjiaHouseItem
from lianjiaSpider.settings import MAX_PAGE

class LianJiaSpider(scrapy.Spider):
    """爬取链家的 信息"""
    name = 'loupan'

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

    # 新房
    loupan_url = 'https://{city}.fang.lianjia.com/loupan/'

    def start_requests(self):
        for city in self.cities:

            # # 新房
            yield scrapy.Request(self.loupan_url.format(city=city),
                                 callback=self.parse_area)

    def parse_area(self, response):
        """添加不同的区域进行爬取数据"""
        base_url = response.url
        sel = scrapy.Selector(response)
        print('sdfsd')
        areas_urls = sel.xpath('//ul[@class="district-wrapper"]/li/@data-district-spell').extract()
        for area_url in areas_urls:
            yield scrapy.Request(base_url + area_url + '/',
                                 callback=self.loupan)

    def loupan(self, response):
        """新房"""
        sel = scrapy.Selector(response)

        lianjia_item = LianjiaHouseItem()
        # url  例：https://cd.lianjia.com/ershoufang/pg1/
        url = response.url
        # # 新房还是二手房 等
        lianjia_item['type'] = url.split('/')[3]
        # 城市
        city = url.split('/')[2].split('.')[0]

        lianjia_item['city'] = city

        lis = sel.xpath('//li[@class="resblock-list"]')
        for li in lis:
            try:
                # 房屋编号
                lianjia_item['house_code'] = li.xpath('./@data-project-name').extract()[0]
                # 标题
                lianjia_item['title'] = li.xpath('.//a[@class="name"]/text()').extract()[0]
                # 图片
                lianjia_item['img_src'] = li.xpath('.//a/img/@src').extract()[0]
                # 在售，下期开售
                lianjia_item['status'] = li.xpath('.//span[@class="sale-status"]/text()').extract()[0]
                # 房屋类型  住宅 别墅
                lianjia_item['house_kind'] = li.xpath('.//span[@class="resblock-type"]/text()').extract()[0]
                # 房屋建面
                lianjia_item['house_area'] = li.xpath('.//div[@class="resblock-area"]/span/text()').extract()[0]
                # 均价
                number = li.xpath('.//span[@class="number"]/text()').extract()[0]
                desc = li.xpath('.//span[@class="desc"]/text()').extract()[0].replace('\xa0', '')
                lianjia_item['unitprice'] = number + ' ' + desc
                # 总价
                lianjia_item['totalprice'] = li.xpath('.//div[@class="second"]/text()').extract()[0]
            except:
                continue

            yield lianjia_item

        # 下一页
        page = int(response.meta.get('page', 1))
        page += 1
        if page > 2:
            url = re.sub('pg\d+/', '', url)
        if page < MAX_PAGE:
            yield scrapy.Request(url + 'pg%d/' % page,
                                 meta={'page': page},
                                 callback=self.loupan)
