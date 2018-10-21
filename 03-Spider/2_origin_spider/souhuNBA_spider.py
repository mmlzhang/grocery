
from urllib.error import URLError
from urllib.request import urlopen

import re
import pymysql
import ssl

from pymysql import Error


def decode_page(page_bytes, charsets=('utf-8',)):
    """解码"""
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError:
            pass
            # logging.error('Decode:', error)
    return page_html


def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
    """获取页面的 HTML 代码 """
    page_html = None
    try:
        page_html = decode_page(urlopen(seed_url).read(), charsets)
    except URLError:
        #logging.error('URL:', error)
        # 出现失败时， 进行重新尝试
        if retry_times > 0:
            get_page_html(seed_url, retry_times=retry_times-1, charsets=charsets)
    return page_html


def get_matched_parts(page_html, pattern_str, pattern_ignore_case=re.I):
    """正则匹配 获取页面中的所有 有用的信息 """
    pattern_regex = re.compile(pattern_str, pattern_ignore_case)
    return pattern_regex.findall(page_html) if page_html else[]


def start_crawl(seed_url, match_pattern, *, max_depth=-1):
    conn = pymysql.connect(host='', port='', database='',
                           user='', password='', charset='')
    try:
        with conn.cursor() as cursor:
            url_list = [seed_url]
            visited_url_list = {seed_url: 0}
            while url_list:
                current_url = url_list.pop(0)
                depth = visited_url_list[current_url]
                if depth != max_depth:
                    page_html = get_page_html(current_url, charsets=('utf-8', 'gbk', 'gb2312'))
                    links_list = get_matched_parts(page_html, match_pattern)
                    param_list = []
                    for link in links_list:
                        if link not in visited_url_list:
                            visited_url_list[link] = depth + 1
                            page_html = get_page_html(link, charsets=('utf-8', 'gbk', 'gb2312'))
                            headings = get_matched_parts(page_html, r'<h1>(.*)<span')
                            if headings:
                                param_list.append((headings[0], links_list))
                    cursor.execute('insert into tb_result values (default, %s, %s)', param_list)
                    conn.commit()
    except Error:
        pass
    finally:
        conn.close()


def main():
    ssl._create_default_https_context = ssl._create_unverified_context()
    url = 'http://sports.sohu.com/nba_a.shtml'
    pattern = r'<a[^>]+test=a\s[^>]*href=["\"](.*?)["\"]'
    start_crawl(url, pattern, max_depth=2)


if __name__ == '__main__':
    main()



