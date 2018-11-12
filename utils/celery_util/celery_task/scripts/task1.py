
import requests
from ..celery import app


def foo_11():
    url = r"http://127.0.0.1:5555/user/celery/?v1=foo_11&v2=bbb"
    requests.get(url)
    print("foo11----------------")

def foo_12():
    url = r"http://127.0.0.1:5555/user/celery/?v1=foo_12&v2=bbb"
    requests.get(url)
    print("foo12--------------")
    foo_11()

@app.task
def celery_run():
    foo_11()
    foo_12()


if __name__ == '__main__':
    celery_run()
