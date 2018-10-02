import os
import redis

from flask import Flask
from flask_session import Session

from APP.user_views import user_blueprint
from APP.hello_views import hello_blueprint
from APP.models import db


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    # 初始化 app
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    # 注册蓝图
    app.register_blueprint(blueprint=hello_blueprint,
                           url_prefix='/hello')

    app.register_blueprint(blueprint=user_blueprint,
                           url_prefix='/user')

    # 设置 密钥  数据库  redis
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'  # 选择数据库类型, 默认连接本地 redis

    # 连接指定的地址, 连接本地, 设置数据库的 地址, 默认的可以不写
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',
                                              port=6379)
    # 添加 sessionid的前缀
    app.config['SESSION_KEY_PREFIX'] = 'flask'

    # 配置数据库 MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql+pymysql://root:123456@localhost:3306/hello_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 导入 session
    # 第一种方式
    # se = Session()
    # se.init_app(app=app)
    # 第二种方式
    Session(app=app)

    # 初始化数据库
    db.init_app(app=app) # 第一种写法

    return app
