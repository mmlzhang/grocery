
from __future__ import absolute_import
from celery import Celery


app = Celery("pj",
             broker="redis://127.0.0.1:6379/1",
             backend="redis://127.0.0.1:6379/2",
             include=["pj.tasks"]
             )
app.config_from_object("pj.config")


if __name__ == '__main__':
    app.start()
