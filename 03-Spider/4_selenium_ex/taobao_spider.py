
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from utils.spider_agents import random_header


def get_html(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = Request(url, headers=headers)
    html = urlopen(req).read()

    return html.decode('utf-8')


def main():

    url = 'https://www.taobao.com/'
    html = get_html(url)
    taobao = BeautifulSoup(html, 'lxml')
    li_list = taobao.find('ul', {'class': 'service-bd'}).find_all('li')
    for li in li_list:
        a_list = li.find_all('a')
        for a in a_list:

            print(a.text, end=': ')
            print(a.attrs['href'])
        print()


if __name__ == '__main__':
    main()