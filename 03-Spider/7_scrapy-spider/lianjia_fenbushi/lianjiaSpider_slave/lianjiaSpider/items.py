# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHouseItem(scrapy.Item):

    type = scrapy.Field()  # 新房还是二手房,或者其他
    city = scrapy.Field()  # 城市
    location = scrapy.Field()  # 区域
    create_time = scrapy.Field()  # 获取信息的时间

    house_code = scrapy.Field()  # 房屋编号
    img_src = scrapy.Field()  # 图片 链接
    title = scrapy.Field()  # 房屋标题
    address = scrapy.Field()  # 房屋地址
    info = scrapy.Field()  #房屋信息
    flood = scrapy.Field()  # 楼盘情况 高层底层  建楼时间
    follower = scrapy.Field()  # 关注者情况 发布时间
    tag = scrapy.Field()  # 地理优势 房屋优势
    totalprice = scrapy.Field()  # 总价 单位：万
    unitprice = scrapy.Field()  # 单价 每平米的价钱

    # 二手房 成交
    trade_time = scrapy.Field()  # 成交周期
    origin_price = scrapy.Field()  # 挂牌价格
    house_year = scrapy.Field()  # 房屋年限  例：房屋满五年

    # 新房
    status = scrapy.Field()  # 房屋状态 在售，下期开售
    house_kind = scrapy.Field()  # 房屋类型  住宅 别墅
    house_area = scrapy.Field()  # 房屋建面

    # 租房
