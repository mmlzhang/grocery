
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import Rule, CrawlSpider

from qidianSpider.items import DoubanspiderItem

from utils.clearn_data import handle

# 继承 CrawlSpider
class DouBanSpider(CrawlSpider):

    name = 'douban'

    # 开始的url
    start_urls = {
        r'https://movie.douban.com/top250'
    }
    # 设置匹配规则
    rules = (Rule(LinkExtractor(allow=r'https://movie.douban.com/top250.*'), callback='parse_item'), ) # 自定义的回调函数


    # def start_requests(self):
    #
    #     for i in range(10):
    #         url = r'https://movie.douban.com/top250?start=%s&filter=' % i * 25
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):

        res = Selector(response)
        items = DoubanspiderItem()
        # 电影名
        items['movie_name'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()').extract()
        # 图片
        items['img'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[1]/a/img/@src').extract()

        # 导演演员信息
        director = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]').extract()
        items['director'] = [handle(info) for info in director]

        # 年份分类信息
        year_type = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]').extract()
        y_c_t_info = [handle(s).split('/') for s in year_type]
        year, country, type = [], [], []
        for y_c_t in y_c_t_info:
            year.append(y_c_t[0])
            country.append(y_c_t[1])
            type.append(y_c_t[2])
        items['year'] = year
        items['country'] = country
        items['type'] = type

        # 评分
        items['rate'] = res.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()').extract()

        return items