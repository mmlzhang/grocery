# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
from urllib.parse import quote


class TabaoSpider(scrapy.Spider):
    name = 'tabao'
    allowed_domains = ['www.taobao.com']
    base_url = 'http://www.taobao.com/'

    def start_requests(self):
        for keyword in self.settings.get("KEYWORDS"):
            for page in self.settings.get("MAX_APGE") + 1:
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)
