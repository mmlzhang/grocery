
import requests

from urllib import parse
from bs4 import BeautifulSoup

from utils.spider_agents import random_header


def get_job_info(url):
    """
    传入 Ajax 的url 获取数据

    :param url:
    :return:
    """
    response = requests.get(url, headers=random_header())

    return


def parse_urlencode(k, v):
    s = parse.urlencode({k: v})
    return s


def get_info(html):
    bsObj = BeautifulSoup(html, 'parser.html')
    pass


def main():
    keywords_list = ['python', ]
    cities_list = ['成都', ]
    position_url = 'https://www.lagou.com/jobs/positionAjax.json?%s&needAddtionalResult=false'
    url = 'https://www.lagou.com/jobs/list_%s?%s&cl=false&fromSearch=true&labelWords=&suginput='
    for keyword in keywords_list:
        for city in cities_list:
            if keyword and city:
                keyword = parse_urlencode('key', keyword).split('=')[1]
                city = parse_urlencode('city', city)
                url = position_url % city
                html = get_job_info(url)


if __name__ == '__main__':
    main()