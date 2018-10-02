from flask import Flask

from user.user_views import user_blueprint
from utils.settings import STATIC_DIR, TEMPLATES_DIR


def create_app():

    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)

    app.register_blueprint(blueprint=user_blueprint,
                           url_prefix='/user')

    return app


