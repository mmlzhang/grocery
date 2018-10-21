
import threading
from concurrent.futures import ThreadPoolExecutor


mylock = threading.BoundedSemaphore(3)


class MyThread(threading.Thread):

    def __init__(self):
        super(MyThread, self).__init__()
        # self.s_name = s_name

    def run(self):
        if mylock.acquire():
            global n
            print('number: %s,  threading name: %s'% (n, self.name))
            n += 1
            mylock.release()


def main():
    thread_list = []
    for i in range(50):
        t1 = MyThread()
        thread_list.append(t1)

    for t in thread_list:
        t.start()


if __name__ == '__main__':
    n = 0
    main()