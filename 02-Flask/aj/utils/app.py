
import redis

from flask import Flask

from aj_app.views import aj_blueprint
from aj_app.user_views import user_blueprint
from aj_app.house_views import house_blueprint
from aj_app.order_view import order_blueprint
from utils.ext_init_app import ext_init
from utils.settings import STATIC_DIR, TEMPLATES_DIR


def create_app():
    """创建  app 并 增加配置"""

    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)

    app.register_blueprint(blueprint=aj_blueprint,
                           url_prefix='/aj')
    app.register_blueprint(blueprint=user_blueprint,
                           url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint,
                           url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint,
                           url_prefix='/order')

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:123456@localhost:3306/aj'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置session
    app.config['SECRET_KEY'] = 'SECRET_KEY'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1',port=6379)
    app.config['SESSION_KEY_PREFIX'] = 'aj-session:'

    ext_init(app)

    return app