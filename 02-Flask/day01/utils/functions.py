from flask import Flask

from user.user_views import blue
from user.stu_views import stu_blue_print

import os


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                template_folder=templates_dir,
                static_folder=static_dir)

    app.register_blueprint(blueprint=blue,  # 注册蓝图
                           url_prefix='/app')  # url 前缀, 加slash /

    app.register_blueprint(blueprint=stu_blue_print,
                           url_prefix='/stu')

    return app