
from __future__ import absolute_import

import requests

from .celery import app


@app.task
def add(x, y):
    url = r"http://127.0.0.1:5555/user/celery/?v1=aaaa&v2=bbb"
    requests.get(url)
    return x + y


@app.task
def subtract(x, y):
    return x -y
