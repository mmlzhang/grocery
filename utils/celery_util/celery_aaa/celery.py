
from __future__ import absolute_import
from celery import Celery


app = Celery("celery_aaa",
             broker="amqp://lanms:123456@localhost/lanms_vhost",
             backend="rpc://",  # 接收运行的结果 result
             include=["celery_aaa.tasks"])
