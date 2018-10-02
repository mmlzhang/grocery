import os

import redis
from flask import Flask

from bs.views import bs
from utils.etx_init import etx_init


def create_app():

    # 静态文件 目录和 模板 目录
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__, static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)

    app.register_blueprint(blueprint=bs,
                           url_prefix='/bs')

    # 配置 session   redis
    app.config['SECRET_KEY'] = 'secret_str'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',
                                              port=6379)
    app.config['SESSION_KEY_PREFIX'] = 'bs-'

    # 配置数据库 mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:123456@localhost:3306/bs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # debugtoolbar
    # app.debug = True
    etx_init(app)

    return app