import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 静态文件
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# 模板
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')