"""

通过 freegeoip.net 的 API 来查找 维基百科中的文章编辑者的分布的国家


"""


import json
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import datetime
import random
import re

from utils.spider_agents import random_header


random.seed(datetime.datetime.now())


def getLinks(articleUrl):
    articleUrl = 'https://en.wikipedia.org' + articleUrl
    req = Request(articleUrl, headers=random_header())
    html = urlopen(req).text
    bsObj = BeautifulSoup(html)

    return bsObj.find('div', {'class': 'bodyContent'}).findAll('a',
                      href=re.compile('^(/wiki/)((?!:).)*$'))


def getHistoryIPs(pageUrl):
    # 编辑历史页面 URL 的格式
    # http://en.wikipedia.org/w/index.php?title=Title_in_url&action=history
    pageUrl = pageUrl.replace('/wiki/', '')
    historyUrl = 'http://en.wikipedia.org/w/index.php?title=' + pageUrl + '&action=history'
    print('historyUrl is : ' + historyUrl)
    req = Request(historyUrl, headers=random_header())
    html = urlopen(req).text
    bsObj = BeautifulSoup(html, 'parser.html')
    # 找出 class 属性是 ‘mw-anonuser’ 的链接
    # 它们 的 IP 地址代替用户名
    ipAddresses = bsObj.findAll('a', {'class': 'mw-anouserlink'})
    addressList = set()
    for ipAdress in ipAddresses:
        addressList.add(ipAdress.get_text())
    return addressList


def getCountry(ipAddress):
    """获取 ipAddress 对应的国家， 通过免费的地图 API """
    try:
        req = Request('http://freegeoip.net/json/' + ipAddress, headers=random_header())
        response = urlopen(req).read().decode('utf-8')
    except Exception:
        return None
    responseJson = json.loads(response)
    return responseJson.get('country_code')


def main():

    links = getLinks('/wiki/Python_(programmig_language)')
    while (len(links) > 0):
        for link in links:
            print('--' * 10)
            historyIPs = getHistoryIPs(link.attrs['href'])
            for historyIP in historyIPs:
                country = getCountry(historyIP)
                if country is not None:
                    print(historyIP + 'if from ' + country)

        newLink = links[random.randint(0, len(links) - 1)].attrs['href']
        links = getLinks(newLink)


if __name__ == '__main__':
    main()
