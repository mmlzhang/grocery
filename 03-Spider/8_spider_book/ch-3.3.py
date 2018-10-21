
import re
import random
import datetime
import time

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from spider_book.user_agent.agents_list import agents


def getInnerLinks(bsObj, includeUrl):
    """获取页面的所有内链列表"""
    internalLinks = []
    # 找出所有以 / 开头的链接
    pattern_str = r'^(/|.*' + includeUrl + ')'
    for link in bsObj.findAll('a', href=re.compile(pattern_str)):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj, excludeUrl):
    """获取页面的外链 列表"""
    externalLinks = []
    pattern_str = r'^(http|www)((?!' + excludeUrl + ').)*$'
    for link in bsObj.findAll('a', href=re.compile(pattern_str)):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link)
    return externalLinks


def splitAddress(address):
    """将传入的 url 以 / 进行切割"""
    addressParts = address.replace('http://', '').split('/')
    return addressParts


def getRandomExternalLink(startingPage):
    """获取随机 链接 """
    header = {
        'User-Agent': agents[random.randint(0, len(agents) - 1)]
    }
    req = Request(startingPage, headers=header)

    html = urlopen(req)
    bsObj = BeautifulSoup(html, 'html.parser')
    rootUrl = splitAddress(startingPage)[0]  # 网站的域名
    externalLinks = getExternalLinks(bsObj, rootUrl)  #获取本网站域名以外的网址
    if len(externalLinks) == 0:
        internalLinks = getInnerLinks(startingPage, rootUrl)   # 拿取页面的一个 内链 进行访问 寻找外链
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite).attrs['href']
    print('随机外链接是：' + externalLink)
    followExternalOnly(externalLink)

def getAllExternalLinks(siteUrl):
    """获取所有的 内链 和 外链 """
    allExtLinks = set()  # 所有的外链
    allInnerLinks = set()  # 所有的内链

    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInnerLinks(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
    for link in internalLinks:
        if link not in allInnerLinks:
            allInnerLinks.add(link)
            getAllExternalLinks(link)

    return (allInnerLinks, allExtLinks)  # 以元组形式返回所有的内链 和 外链


def main():
    # 没有进行去重操作，还有异常的处理也需要增加

    startingSite = 'http://oreilly.com'
    followExternalOnly(startingSite)


if __name__ == '__main__':
    main()
