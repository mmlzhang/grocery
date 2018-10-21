
import time

from concurrent.futures import ThreadPoolExecutor


def add100(num):
    print('我是 + 100 ')
    return num + 100


def add1000(future):
    print('我是 + 1000')
    num = future.result()
    time.sleep(5)
    print(num + 1000)


def main():
    pool = ThreadPoolExecutor(3)
    for num in range(1,50):
        print('开始计算数字：%s ！' % num)
        future = pool.submit(add100, num)
        future.add_done_callback(add1000)  # 前面的结果返回后进行下个函数的调用


if __name__ == '__main__':
    main()