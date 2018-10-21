
import time


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] 消费者：%s' % n)
        time.sleep(1)
        r = 'CONSUMER，结束状态！'


def produce(c):
    next(c)  # 启动程序 ，让执行到 yield 处， 暂停, 等待
    n = 0
    while n < 3:
        n += 1
        print('n的值：%s...' % n)
        # 将 n 传入到 yield 中， yield r 的值 替换为 n，
        # 同时 将原来的r 的值获取到， 赋值给当前的 r
        r = c.send(n)
        print('r的值：%s' % r)
        print('--' * 20)
    c.close()


def main():
    c = consumer()
    produce(c)


if __name__ == '__main__':
    main()
