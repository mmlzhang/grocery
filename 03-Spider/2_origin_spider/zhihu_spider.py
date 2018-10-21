
import requests
from lxml import etree
from bs4 import BeautifulSoup


def start_crawl(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    # print(res.text)
    # etree 解析
    # html = etree.HTML(res.text)
    # a = html.xpath('//*[@id="zh-recommend-list"]/div[3]/h2/a')
    # print(a)

    # BeautifulSoup 解析
    soup = BeautifulSoup(res.text)
    soup.findAll()
    result = soup.find_all('a', {'class': 'question_link'})
    # print(a)
    for i in result:
        print()
        s = i.get_text()
        print(s)


def main():
    url = r'https://www.zhihu.com/explore'
    start_crawl(url)


if __name__ == '__main__':
    main()