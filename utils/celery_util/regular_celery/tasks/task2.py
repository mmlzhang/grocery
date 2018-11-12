
import requests
from ..celery import app


def foo_21(v1, v2):
    url = r"http://127.0.0.1:8800/user/celery/?v1={}&v2={}".format(v1, v2)
    requests.get(url)
    print("foo_21----------------")


# def foo_22():
#     url = r"http://127.0.0.1:8800/user/celery/?v1=foo_22&v2=bbb"
#     requests.get(url)
#     print("foo_22--------------")
#     foo_21()


@app.task
def celery_run(v1="foo_21", v2="22222"):
    print("Task2 正在运行！！")
    foo_21(v1, v2)
    # foo_22()
    print("Task2 结束！！")


if __name__ == '__main__':
    celery_run()
