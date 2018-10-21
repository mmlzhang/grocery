
import scrapy

from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.items import LianjiaHouseItem


class LianJiaSpider(RedisSpider):
    """爬取链家 租房"""
    name = 'zufang'
    redis_key = 'lianjia:zufang'

    def parse(self, response):
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
                print('>>>>' * 20)
                print('zufang', city)
                print(url)
                print('>>>>' * 20)
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

