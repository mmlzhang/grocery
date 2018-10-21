
import scrapy

from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.items import LianjiaHouseItem


class LianJiaSpider(RedisSpider):
    """爬取链家的 成交 信息"""
    name = 'chenjiao'
    redis_key = 'lianjia:chanjiao'

    def parse(self, response):
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
                print('>>>>' * 20)
                print('成交', city)
                print(url)
                print('>>>>' * 20)
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

