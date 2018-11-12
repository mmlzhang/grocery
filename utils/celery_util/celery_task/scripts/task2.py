
import requests
from ..celery import app


def foo_21():
    url = r"http://127.0.0.1:5555/user/celery/?v1=foo_21&v2=bbb"
    requests.get(url)
    print("foo_21----------------")


def foo_22():
    url = r"http://127.0.0.1:5555/user/celery/?v1=foo_22&v2=bbb"
    requests.get(url)
    print("foo_22--------------")
    foo_21()


@app.task
def celery_run():
    foo_21()
    foo_22()


if __name__ == '__main__':
    celery_run()
