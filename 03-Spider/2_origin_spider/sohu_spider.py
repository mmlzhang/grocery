
import re

from urllib.request import urlopen, Request
from lxml import etree


def decode_page(page_bytes, charsets=('utf-8',)):
    """ 解码 页面 """
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break   # 解析出正取的页面时, 跳出循环
        except UnicodeDecodeError as e:
            # logging.error('Decoder': e)
            pass
            # print('编码错误')
    if page_html:
        return page_html
    else:
        print('解码错误!')


def get_matched_parts(page_html, pattern_str, flags=re.S):
    """正则匹配, 获取需要的部分"""
    pattern_regex = re.compile(pattern_str, flags)
    return pattern_regex.findall(page_html) if page_html else []


def matched_by_lxml(html, xpath):

    lxml_html = etree.HTML(html)
    result = lxml_html.xpath(xpath)
    news_list = []
    for i in result:

        url = i.xpath('./@href')[0]
        title = i.xpath('./text()')[0]
        news_list.append((url, title))

    return news_list


def get_page_html():
    page_html = None


def start_crawl(url, xpath):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = Request(url, headers=headers)
    res = urlopen(req)
    page = res.read()
    page_html = decode_page(page, charsets=('utf-8', 'gbk'))
    result = matched_by_lxml(page_html, xpath=xpath)
    return result


def main():
    url = r'http://sports.sohu.com/nba_a.shtml'
    xpath = '/html/body/div[1]/div[4]/div[1]/div[1]/ul/li/a'
    news_list = start_crawl(url, xpath)
    for url, title in news_list:
        print(url)
    # with open('test.txt', 'w', encoding='utf-8') as f:
    #     f.write(o)


if __name__ == '__main__':
    main()