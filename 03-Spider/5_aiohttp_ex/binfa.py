
import time
import datetime
import asyncio
from aiohttp import ClientSession


# def hello():
#     time.sleep(1)


# def run():
#     bg = datetime.datetime.now()
#     for i in range(5):
#         hello()
#     t = datetime.datetime.now() - bg
#     print('耗时：%s' % t)
#
#
# def main():
#     run()
#
#
# if __name__ == '__main__':
#     main()



tasks = []

url = 'https://www.baidu.com/{}'

async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)


def run():
    for i in range(5):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)


def main():
    bg = datetime.datetime.now()

    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))

    end = datetime.datetime.now()
    print('耗时：%s' % (end - bg))


if __name__ == '__main__':
    main()

