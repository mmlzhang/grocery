
import scrapy

from scrapy_redis.spiders import RedisSpider
from lianjiaSpider.items import LianjiaHouseItem


class LianJiaSpider(RedisSpider):
    """爬取链家的 二手房 信息"""
    name = 'ershoufang'

    redis_key = 'lianjia:ershoufang'

    def parse(self, response):
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
        # location = response.meta.get('location')
        # lianjia_item['location'] = location

        lis = sel.xpath('/html/body/div[4]/div[1]/ul/li[@class="clear"]')
        for li in lis:
            try:
                print('>>>>' * 20)
                print('二手房', city)
                print(url)
                print('>>>>' * 20)
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
