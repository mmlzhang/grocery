
import scrapy

from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.items import LianjiaHouseItem


class LianJiaSpider(RedisSpider):
    """爬取链家 楼盘"""
    name = 'loupan'
    redis_key = 'lianjia:loupan'

    def parse(self, response):
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
                print('>>>>' * 20)
                print('xinfang', city)
                print(url)
                print('>>>>' * 20)
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

