import re

import scrapy

from lianjiaSpider.items import LianjiaHouseItem
from lianjiaSpider.settings import MAX_PAGE


class LianJiaSpider(scrapy.Spider):
    """爬取链家的 信息"""
    # name = 'ershoufang'

    # 允许访问的域名，爬取的域名
    # allowed_domains = ['lianjia.com']

    """
    北京(bj) 上海(sh) 深圳(sz) 成都(cd) 重庆(cq) 长沙(cs) 大连(dl) 德阳(dy) 广州(gz) 杭州(hz) 
    海口(hk) 合肥(hf) 济南(jn) 昆明(km) 南京(nj) 青岛(qd) 苏州(sz) 石家庄(sjz) 沈阳(sy) 天津(tj)
    太原(ty) 武汉(wh) 厦门(xm) 西安(xa) 郑州(zz)
    """
    # 24 个 目标 城市
    # cities = [
    #     'bj', 'sh', 'sz', 'cd', 'cq', 'cs', 'dl', 'dy', 'gz',
    #     'hz', 'hk', 'hf', 'jn', 'km', 'nj', 'qd', 'sz', 'sjz',
    #     'sy', 'tj', 'ty', 'wh', 'xm', 'xa', 'zz',
    # ]

    # 测试城市
    cities = ['cd']

    redis_key = 'lianjia:start_urls'

    # 二手房 房源
    ershoufang_url = 'https://{city}.lianjia.com/ershoufang/'

    def start_requests(self):
        for city in self.cities:
            # 二手房
            yield scrapy.Request(self.ershoufang_url.format(city=city),
                                 callback=self.parse_area)

    def parse_area(self, response):
        """添加不同的区域进行爬取数据"""
        base_url = response.url
        sel = scrapy.Selector(response)

        areas_urls = sel.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for area_url in areas_urls:
            area_url = area_url.replace('/ershoufang/', '')
            yield scrapy.Request(base_url + area_url,
                                 meta={'location': area_url},
                                 callback=self.parse_house_info)

    def parse_house_info(self, response):
        """二手房 房屋信息"""
        sel = scrapy.Selector(response)

        lianjia_item = LianjiaHouseItem()
        # url  例：https://cd.lianjia.com/ershoufang/pg1/
        url = response.url
        # # 新房还是二手房
        lianjia_item['type'] = url.split('/')[3]
        # 城市
        city = url.split('/')[2].split('.')[0]
        lianjia_item['city'] = city
        # 城市的区域
        location = response.meta.get('location')
        lianjia_item['location'] = location

        lis = sel.xpath('/html/body/div[4]/div[1]/ul/li[@class="clear"]')
        for li in lis:
            try:
                # 房屋编号
                lianjia_item['house_code'] = li.xpath('./a/@data-housecode').extract()[0]
                if li.xpath('./a/img/@src'):
                    # 图片 链接
                    lianjia_item['img_src'] = li.xpath('./a/img/@src').extract()[0]
                # 房屋标题
                lianjia_item['title'] = li.xpath('./div/div/a/text()').extract()[0]
                # 房屋地址
                lianjia_item['address'] = li.xpath('./div/div[2]/div/a/text()').extract()[0]
                #房屋信息
                info = li.xpath('./div/div[2]/div/text()').extract()[0]
                lianjia_item['info'] = [i.strip() for i in info.split('|')[1:]]
                # 楼盘情况 高层底层  建楼时间
                flood = li.xpath('.//div[@class="flood"]/div/text()').extract()[0]
                lianjia_item['flood'] = flood.replace(' ', '').replace('-', '')
                # 关注者情况 发布时间
                follower = li.xpath('.//div[@class="followInfo"]/text()').extract()[0]
                lianjia_item['follower'] = follower.replace(' ', '').split('/')
                # 地理优势 房屋优势
                lianjia_item['tag'] = li.xpath('.//div[@class="tag"]/span/text()').extract()[0]
                # 总价 单位：万
                lianjia_item['totalprice'] = li.xpath('.//div[@class="totalPrice"]/span/text()').extract()[0] + ' 万'
                # 单价 每平米的价钱
                lianjia_item['unitprice'] = li.xpath('.//div[@class="unitPrice"]/span/text()').extract()[0]
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
                                 callback=self.parse_house_info)
