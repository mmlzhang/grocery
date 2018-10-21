
import time
import datetime
import asyncio
from aiohttp import ClientSession


tasks = []

url = 'https://www.baidu.com/{}'


def hello(url):
        with ClientSession().get(url) as response:
            response = response.read()


def run():
    for i in range(5):
        hello(url.format(str(i)))


def main():
    bg = datetime.datetime.now()
    run()
    end = datetime.datetime.now()
    print('耗时：%s' % (end - bg))


if __name__ == '__main__':
    main()

