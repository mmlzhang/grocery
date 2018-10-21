"""

获取 网页的图片并且保存在本地

"""



import os

from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup

from utils.spider_agents import random_header


def getAbsoluteURL(baseUrl, source):
    """
    将所有传入的url变为以 http:// 开头，并且将所有的包含有 baseUrl 的链接返回
    有 baseUrl 说明就是本站内的 url
     """
    url = ''
    if source.startwith('http://www.'):
        url = 'http://' + source[11:]
    elif source.startwith('http://'):
        url = source
    elif source.startwith('www.'):
        url = source[4:]
        url = 'http://' + source
    if baseUrl not in url:
        return None
    return url


def getDownLoadPath(baseUrl, absoluteUrl, downloadDirectory):
    """
    组装下载的 保存文件 路径 （其实是最后保存时的文件名）  并且判断创建 保存文件的 文件目录
    :param baseUrl:
    :param absoluteUrl:
    :param downloadDirectory:
    :return:
    """
    path = absoluteUrl.replace('www.', '')
    path = path.replace(baseUrl, '')
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.mkdir(directory)
    return path


def main():

    baseurl = 'http://www.pythonscraping.com'
    downloadDirectory = 'downloaded'
    req = Request(baseurl, headers=random_header())
    html = urlopen(req)
    bsObj = BeautifulSoup(html.text, 'parser.html')
    downloadList = bsObj.findAll(src=True)

    for download in downloadList:
        fileUrl = getAbsoluteURL(baseurl, download['src'])
        if fileUrl is not None:
            print(fileUrl)
            save_path = getDownLoadPath(baseurl, fileUrl, downloadDirectory)
            urlretrieve(fileUrl, save_path)


if __name__ == '__main__':
    main()