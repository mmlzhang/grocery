
import asyncio
import time
import types


async def sleep_2_s():
    time.sleep(2)


@asyncio.coroutine
def func():
    print('休眠 2 秒')
    t = yield from sleep_2_s()


async def foo():
    print('休眠 3 秒')
    time.sleep(3)


# @asyncio.coroutine
# def hello(n):
#     print('hello, world! ' + n)
#     r = yield from func()  # 等待 4 s 但是程序马上启动了第二个任务
#     print('hello complete! ' + n)

async def hello(n):
    print('hello, world! ' + n)
    # await asyncio.sleep(3)
    # await foo()
    await func()
    print('结束 ：' + n )


def main():

    loop = asyncio.get_event_loop()
    tasks = []
    for t in [hello('first'), hello('second'), hello('third')]:
        e = asyncio.ensure_future(t)
        tasks.append(e)
    task = asyncio.wait()
    loop.run_until_complete(task)
    loop.close()


if __name__ == '__main__':
    main()

