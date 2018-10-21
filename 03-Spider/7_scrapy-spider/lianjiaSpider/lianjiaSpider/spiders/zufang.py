import re

import scrapy

from lianjiaSpider.items import LianjiaHouseItem
from lianjiaSpider.settings import MAX_PAGE


class LianJiaSpider(scrapy.Spider):
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
        print('sdfs')
        areas_urls = sel.xpath('//div[@class="option-list"]/a/@href').extract()
        for area_url in areas_urls:
            area_url = area_url.replace('/zufang/', '')
            yield scrapy.Request(base_url + area_url,
                                 callback=self.parse_zufang)

    def parse_zufang(self, response):
        """租房"""
        sel = scrapy.Selector(response)

        lianjia_item = LianjiaHouseItem()
        # url  例：https://cd.lianjia.com/ershoufang/pg1/
        url = response.url
        # # 新房还是二手房等
        lianjia_item['type'] = url.split('/')[3]
        # 城市
        city = url.split('/')[2].split('.')[0]
        lianjia_item['city'] = city

        lis = sel.xpath('//ul[@class="house-lst"]/li')
        for li in lis:
            try:
                # 房屋编号
                lianjia_item['house_code'] = li.xpath('./@data-housecode').extract()[0]
                if li.xpath('.//div[@class="pic-panel"]/a/img/@src'):
                    # 图片 链接
                    lianjia_item['img_src'] = li.xpath('.//div[@class="pic-panel"]/a/img/@src').extract()[0]
                # 房屋标题
                lianjia_item['title'] = li.xpath('.//div[@class="info-panel"]/h2/a/text()').extract()[0]
                # 房屋地址
                info = li.xpath('.//div[@class="where"]//text()').extract()
                address = info[0].replace('\xa0','')
                hous_info = ''.join(info[1:]).replace('\xa0',' ')
                lianjia_item['address'] = address
                # 房屋信息
                lianjia_item['info'] = hous_info
                # 租楼情况 高层底层  建楼时间 例：攀成钢租房/低楼层(共33层)/2009年建塔楼
                flood = li.xpath('.//div[@class="con"]//text()').extract()
                lianjia_item['flood'] = ''.join(flood)
                # 关注者情况
                follower = li.xpath('.//div[@class="col-2"]//text()').extract()
                lianjia_item['follower'] = ''.join(follower)
                # 地理优势 房屋优势
                tag = li.xpath('.//div[@class="view-label left"]//text()').extract()
                lianjia_item['tag'] = '#'.join(tag)
                # 单价
                price = li.xpath('.//div[@class="price"]//text()').extract()
                lianjia_item['unitprice'] = ' '.join(price)
            except:
                continue

            yield lianjia_item

        # 下一页
        s = url
        page = int(response.meta.get('page', 1))
        page += 1
        if page > 2:
            url = re.sub('pg\d+/', '', url)
        if page < MAX_PAGE:
            yield scrapy.Request(url + 'pg%d/' % page,
                                 meta={'page': page},
                                 callback=self.parse_zufang)
