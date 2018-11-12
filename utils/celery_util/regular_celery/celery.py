
from __future__ import absolute_import  # 拒绝隐式引入，因为celery.py的名字和celery的包名冲突，需要使用这条语句让程序正确地运行
from celery import Celery

# 创建celery应用对象
app = Celery("my_regular")

# 导入celery的配置信息
app.config_from_object("regular_celery.config")


##################################################
# 启动命令
# celery -A regular_celery flower  # 启动可视化界面 flower 5555端口
# celery -A regular_celery beat  # 发布任务
# celery -A regular_celery worker --loglevel=info  # 执行任务
# celery -B -A regular_celery worker --loglevel=info  # 发布并执行任务
#
#
#
##################################################
