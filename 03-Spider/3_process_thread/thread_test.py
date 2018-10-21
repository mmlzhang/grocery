

import threading
import time


class Study(threading.Thread):

    def __init__(self, name):
        super(Study, self).__init__()
        self.s_name = name

    def run(self):  # 重构方法
        print('当前线程名称- %s' % threading.current_thread().name)
        print('开始学习！- %s' % self.s_name)
        time.sleep(3)
        print('学习结束')
        print('当前线程名称- %s' % threading.current_thread().name)
        # print('---' * 20)


def main():

    s1 = Study('语文')
    s2 = Study('数学')

    # 守护线程  在 start 前  主线程结束 子线程会被强制结束
    # s1.daemon = True
    # s2.daemon = True

    # s1.start()
    # 阻塞
    # s1.join()  # 阻塞在这里  等 s1 结束 再向下执行程序

    # s2.start()

    s1.run()   # 都变为主线程  程序会顺序执行， 不存在同时执行
    s2.run()   # 相当于只是在执行函数， 并没有使用 多线程

    print('测试结束-----')

    # s1.run()


if __name__ == '__main__':
    main()
