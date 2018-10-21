
import re
import random
import datetime
import time

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from spider_book.user_agent.agents_list import agents


def getLinks(articalUrl):
    header = {
        'User-Agent': agents[random.randint(0, len(agents) -1 )]
    }
    url = 'https://en.wikipedia.org' + articalUrl
    req = Request(url, headers=header)
    html = urlopen(req)
    bsObj = BeautifulSoup(html, 'html.parser')
    try:
        title = bsObj.h1.get_test
        first_chapter = bsObj.find(id='mw-content-text').findAll('p')[0]
        edit_url = bsObj.find(id='ca-edit').find('span').find('a').attrs['href']
        print('edit_url:', edit_url)
    except AttributeError:
        pass

    link_list = bsObj.find('div', {'id': 'bodyContent'}).findAll('a',
                           href=re.compile(r'^(/wiki/)((?!:).)*$'))
    return link_list


def main():
    articalUrl = '/wiki/Kevin_Bacon'
    links = getLinks(articalUrl)
    pages = set()  # 去重  避免重复采集
    random.seed(datetime.datetime.now())  # 产生随机数种子
    while(len(links)) > 0:
        newUrl = links[random.randint(0, len(links) - 1)].attrs['href']
        if newUrl not in pages:  # 去重
            print(newUrl)
            pages.add(newUrl)
            time.sleep(random.randint(5, 10))
            links = getLinks(newUrl)


if __name__ == '__main__':
    main()
