
import scrapy
from scrapy.selector import Selector



class QiDianSpider(scrapy.Spider):
    # 启动项目制定的name参数
    name = 'qidian'
    # 需要爬取的页面
    start_urls = {
        'https://www.qidian.com/',
    }

    # def start_requests(self):
    #     urls = {
    #         'https://www.qidian.com/',
    #     }
    #
    #     for url in urls:
    #


    # 解析页面
    def parse(self, response):
        print('>>' * 40)

        # 请求时的 url
        current_url = response.url
        # 返回的 THML 页面
        body = response.body


        # 返回的html unicode编码
        unicode_body = response.body_as_unicode()

        # 小说分类信息
        res = Selector(response)
        menu_type = res.xpath('//*[@id="classify-list"]/dl/dd/a/cite/span/i/text()').extract()
        menu_type_href = res.xpath('//*[@id="classify-list"]/dl/dd/a/@href').extract()
        print(type(menu_type_href[0]))
        print(menu_type, menu_type_href)

        print('<<<<' * 40)
        return response