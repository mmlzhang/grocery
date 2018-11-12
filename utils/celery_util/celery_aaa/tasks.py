
from __future__ import absolute_import
from .celery import app
import time


@app.task
def longtime_add(x, y):
    print("开始运行任务：longtime_add!")
    time.sleep(2)
    print("time sleep finish")
    return x + y


if __name__ == '__main__':
    longtime_add.delay(1, 2)
