
import threading
import datetime
import time


class CountThread(threading.Thread):

    def __init__(self, range_num):   # 传入的 range_number 是一个元组
        # 查找所有的超类， 以及超类的超类， 直到找到所需的属性
        super(CountThread, self).__init__()
        self.begin, self.end  = range_num
        self.result = 0

    def run(self):
        counter = 0
        for i in range(self.begin, self.end):
            counter += i
        self.result += counter

    def get_result(self):
        return self.result


def main():
    begin = datetime.datetime.now()

    result = 0
    num_list = [(0, 10000000), (10000001, 20000000), (20000001, 30000000), (30000001, 40000000)]
    thread_list = []
    for range_num in num_list:
        thread_list.append(CountThread(range_num))

    for t in thread_list:
        t.start()
        t.join()
        result += t.get_result()

    print(result)
    end = datetime.datetime.now()
    print('共计使用时间：%s' % (end - begin))


if __name__ == '__main__':
    main()