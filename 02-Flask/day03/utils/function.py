import os
import redis

from flask import Flask

from App.views import user_blueprint
from utils.ext_app import ext_init


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    template_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__, static_folder=static_dir,
                template_folder=template_dir)

    app.register_blueprint(blueprint=user_blueprint,
                           url_prefix='/user')

    # 配置 session
    # 设置 密钥  数据库  redis
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'  # 选择数据库类型, 默认连接本地 redis

    # 连接指定的地址, 连接本地, 设置数据库的 地址, 默认的可以不写
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',
                                              port=6379)
    # 添加 sessionid的前缀
    app.config['SESSION_KEY_PREFIX'] = 'day03-'

    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:123456@localhost:3306/hello_flask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.debug = True

    ext_init(app)

    return app



