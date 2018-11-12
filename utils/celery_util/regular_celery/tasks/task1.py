
import requests
from ..celery import app


def foo_11(v1, v2):
    url = r"http://127.0.0.1:8800/user/celery/?v1={}&v2={}".format(v1, v2)
    requests.get(url)
    print("foo11----------------")


# def foo_12():
#     url = r"http://127.0.0.1:8800/user/celery/?v1=foo_12&v2=bbb"
#     requests.get(url)
#     print("foo12--------------")
#     foo_11()


@app.task
def celery_run(v1="foo_11", v2="11111"):
    print("Task1 正在运行！！")
    foo_11(v1, v2)
    # foo_12()
    print("Task1 结束！！")


if __name__ == '__main__':
    celery_run()
