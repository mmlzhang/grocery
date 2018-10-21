
import scrapy
from xiciIPSpider.items import XiciipspiderItem


class xiciSpider(scrapy.Spider):
    name='xici'

    start_list = []
    for i in range(1,10):
        url = r'http://www.xicidaili.com/nn/%s' % str(i)
        start_list.append(url)
    start_urls=start_list

    def start_requests(self):
        user_agent ="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        headers= {'User-Agent':user_agent}
        for url in self.start_list:
            yield scrapy.Request(url=url,headers=headers,method='GET',callback=self.parse)

    def parse(self, response):
        #//*[@id="ip_list"]
        #tdinfo.xpath('td[2]/text()')[0].extract()
        #<a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
        #re
        #response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')

        lists=response.xpath('//*[@id="ip_list"]/tr')
        # print(lists)
        with open('xici.txt', "a", encoding='utf-8') as wd:
            for index, tdinfo in enumerate(lists):
                if index != 0:
                    # xiciI = xiciItem()
                    # xiciI['ipaddress'] = tdinfo.xpath('td[2]/text()').extract_first()
                    # xiciI['dk'] = tdinfo.xpath('td[3]/text()').extract_first()
                    # yield xiciI
                    ipline = tdinfo.xpath('td[2]/text()').extract_first() +":"+tdinfo.xpath('td[3]/text()').extract_first()
                    print(ipline)
                    wd.write(ipline+u"\n")
