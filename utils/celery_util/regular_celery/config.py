from __future__ import absolute_import # 拒绝隐式引入，因为celery.py的名字和celery的包名冲突，需要使用这条语句让程序正确地运行
from celery.schedules import crontab, timedelta
from kombu import Queue


# Redis
broker_url = "redis://127.0.0.1:6379/5"
result_backend = "redis://127.0.0.1:6379/6"

# RabbitMQ
# broker_url = "amqp://lanms:123456@localhost/lanms_vhost"
# result_url = "rpc://"

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = True  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60  # 存储结果过期时间（默认1天 60 * 60 * 24）

# 每个worker执行了多少任务就会死掉
worker_max_tasks_per_child = 40
# 如果对结果不关心，或者任务的执行本身会对数据产生影响
task_ignore_result = False

# broker 到 worker 的设置
# broker_transport_options = {
#     "visibility_timeout": 10,  # 设置时间限制 1小时
# }

# 导入任务所在文件
imports = [
    "regular_celery.tasks.task1",  # 导入py文件
    "regular_celery.tasks.task2",
]

# 参数
v1 = 'sss'
v2 = "aaa"

# # 需要执行任务的配置
beat_schedule = {
    "task1": {
        "task": "regular_celery.tasks.task1.celery_run",  # 执行的函数
        # "schedule": crontab(minute="*/1"),   # every minute 每分钟执行
        "schedule": timedelta(seconds=3),  # 3秒执行一次
        "args": (v1, v2)  # # 任务函数参数
    },
    # "task2": {
    #     "task": "regular_celery.tasks.task2.celery_run",
    #     # "schedule": crontab(minute=0, hour="*/1"),   # every minute 每小时执行
    #     "schedule": timedelta(seconds=5),
    #     "args": ()
    # },
}


# 异步任务
# # 导入Queue
# from kombu import Queue
# # 导入Task所在的模块，所有使用celery.task装饰器装饰过的函数，所需要把所在的模块导入
# # 我们之前创建的几个测试用函数，都在handlers.async_tasks和handlers.schedules中
# # 所以在这里需要导入这两个模块，以str表示模块的位置，模块组成tuple后赋值给CELERY_IMPORTS
# # 这样Celery在启动时，会自动找到这些模块，并导入模块内的task
# CELERY_IMPORTS = ('handlers.async_tasks', 'handlers.schedules')
# # 为Celery设定多个队列，CELERY_QUEUES是个tuple，每个tuple的元素都是由一个Queue的实例组成
# # 创建Queue的实例时，传入name和routing_key，name即队列名称
# CELERY_QUEUES = (
#     Queue(name='email_queue', routing_key='email_router'),
#     Queue(name='message_queue', routing_key='message_router'),
#     Queue(name='schedules_queue', routing_key='schedules_router'),
# )
# # 最后，为不同的task指派不同的队列
# # 将所有的task组成dict，key为task的名称，即task所在的模块，及函数名
# # 如async_send_email所在的模块为handlers.async_tasks
# # 那么task名称就是handlers.async_tasks.async_send_email
# # 每个task的value值也是为dict，设定需要指派的队列name，及对应的routing_key
# # 这里的name和routing_key需要和CELERY_QUEUES设定的完全一致
# CELERY_ROUTES = {
#     'handlers.async_tasks.async_send_email': {
#         'queue': 'email_queue',
#         'routing_key': 'vcan.email_router',
#     },
#     'handlers.async_tasks.async_push_message': {
#         'queue': 'message_queue',
#         'routing_key': 'message_router',
#     },
#     'handlers.schedules.every_30_seconds': {
#         'queue': 'schedules_queue',
#         'routing_key': 'schedules_router',
#     }
# }
# # 配置完成后，不同的task会根据CELERY_ROUTES的设置，指派到不同的消息队列。
