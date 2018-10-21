
import json

import scrapy


class LagouSpider(scrapy.Spider):

    name = 'lagou'

    def start_requests(self):
        form_data = {'pn': '1', 'kd': 'python'}
        url = r'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'
        yield scrapy.FormRequest(url=url, formdata=form_data, callback=self.parse)

    def parse(self, response):

        res = json.loads(response.text)
        pass