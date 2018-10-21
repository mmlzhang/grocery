import re

import scrapy

from lianjiaSpider.items import LianjiaHouseItem
from lianjiaSpider.settings import MAX_PAGE


class LianJiaSpider(scrapy.Spider):
    """爬取链家的 信息"""
    name = 'chenjiao'

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

   # 二手房，成交
    chenjiao_url = 'https://{city}.lianjia.com/chengjiao/'

    def start_requests(self):
        for city in self.cities:
            # 二手房成交
            yield scrapy.Request(self.chenjiao_url.format(city=city),
                                 callback=self.parse_area)

    def parse_area(self, response):
        """添加不同的区域进行爬取数据"""
        base_url = response.url
        sel = scrapy.Selector(response)

        areas_urls = sel.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for area_url in areas_urls:
            area_url = area_url.replace('/chengjiao/', '')
            yield scrapy.Request(base_url + area_url,
                                 callback=self.parse_chenjiao)

    def parse_chenjiao(self, response):
        """二手房成交"""
        sel = scrapy.Selector(response)

        lianjia_item = LianjiaHouseItem()
        # url  例：https://cd.lianjia.com/ershoufang/pg1/
        url = response.url
        # # 新房还是二手房 等
        lianjia_item['type'] = url.split('/')[3]
        # 城市
        city = url.split('/')[2].split('.')[0]
        lianjia_item['city'] = city

        lis = sel.xpath('//ul[@class="listContent"]/li')
        for li in lis:
            try:
                # 标题
                title = li.xpath('.//div[@class="title"]/a/text()').extract()[0]
                lianjia_item['title'] = title
                lianjia_item['house_code'] = title
                # 房屋编号  从 title 中获取 <a href="https://cd.lianjia.com/chengjiao/106101178880.html" target="_blank">中铁丽景书香 1室0厅 36.97平米</a>
                # 有的房屋没有编号，暂时不用
                # href = li.xpath('./@data-project-name').extract()
                # if href:
                #     lianjia_item['house_code'] = href[0].split('/')[-1].split('.')[0]
                # else:
                #     lianjia_item['house_code'] = title
               # 图片
                lianjia_item['img_src'] = li.xpath('.//img[@class="lj-lazy"]/@src').extract()[0]
                # 楼盘情况 高层底层  建楼时间
                lianjia_item['flood'] = li.xpath('.//div[@class="positionInfo"]/text()').extract()[0]
                # 房屋年限，已近购买满几年
                lianjia_item['house_year'] = li.xpath('.//span[@class="dealHouseTxt"]/span/text()').extract()[0]
                # 地理优势 房屋优势
                tag = li.xpath('.//div[@class="houseInfo"]/text()').extract()[0]
                lianjia_item['tag'] = tag.replace('\xa0','').replace('|', '')
                # 挂牌价格
                lianjia_item['origin_price'] = li.xpath('.//span[@class="dealCycleTxt"]/span[1]/text()').extract()[0]
                # 成交周期
                lianjia_item['trade_time'] = li.xpath('.//span[@class="dealCycleTxt"]/span[2]/text()').extract()[0]

                # 交易价格 暂无
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
                                 callback=self.parse_chenjiao)
