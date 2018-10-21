
import urllib.request
from urllib import parse


def main(url):
    header = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=header)
    res = urllib.request.urlopen(req)

    return res.read().decode('utf-8')


if __name__ == '__main__':
    msg = input('搜索信息：')
    search = parse.urlencode({'wd': msg})
    print(search)
    url = 'https://www.baidu.com/s?%s' % search
    result = main(url)
    print(result)
