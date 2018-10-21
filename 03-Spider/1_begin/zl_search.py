
import re

import urllib.request
from urllib import parse


def get_zhilian_html(url, search):
    url = url + search
    header = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      r'AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/63.0.3239.132 Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=header)
    res = urllib.request.urlopen(req)

    return res.read().decode('utf-8')


def get_job_num(html):
    """职位的总数"""
    num = re.findall(r'<em>(\d+)</em>', html)
    return num if num else 0
"""   ./"""

def get_company_name(html):
    """获取公司名称"""
    pattern = re.compile(r'^<td class="gsmc"><a href="(.*?)" target="_blank">(.*?)</a> <a href$', re.S)
    name = re.findall(pattern, html)
    return name


def main():

    # city = input('搜索的城市：')
    # job = input('搜索的岗位：')
    city = '成都'
    job = 'python'
    search = parse.urlencode({'jl': city, 'kw': job})
    url = r'https://sou.zhaopin.com/jobs/searchresult.ashx?'
    html = get_zhilian_html(url, search)
    job_num = get_job_num(html)
    name = get_company_name(html)

    print(name)


if __name__ == '__main__':
    main()
