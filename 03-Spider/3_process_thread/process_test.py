
import os
import time
import random

from multiprocessing import Process


def coding():
    while True:
        print('AAAAAA, 进程号：%s' % os.getpid())
        time.sleep(random.randint(1, 5))
        print('BBBBBBB， 进程号：%s' % os.getpid())


def play():
    while True:
        print('1111111111， 进程号：%s' % os.getpid())
        time.sleep(random.randint(1, 5))
        print('2222222222， 进程号：%s' % os.getpid())


def main():
    p1 = Process(target=coding)
    p2 = Process(target=play)

    p1.start()   # 进程之间在不阻塞的情况下是没有影响的，
    # 阻塞   等执行完才会进行下一个
    # p1.join()
    p2.join()

    p2.start()


if __name__ == '__main__':
    main()

