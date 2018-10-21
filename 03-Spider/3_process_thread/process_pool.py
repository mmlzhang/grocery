
import time

from multiprocessing import Process, Array


def task(num, li):
    time.sleep(1)
    li[num] = num
    print(list(li))


def main():
    li = Array('i', 10)
    for i in range(10):
        p = Process(target=task, args=(i, li))
        # p.daemon = True
        p.start()
        # p.join()
    print('主进程结束！！！')


if __name__ == '__main__':
    main()