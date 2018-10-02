from flask_session import Session
from flask_restful import Api
from flask_debugtoolbar import DebugToolbarExtension

from bs.models import db


toolbar = DebugToolbarExtension()
api = Api()
se = Session()


def etx_init(app):

    # Session(app=app)
    se.init_app(app=app)
    db.init_app(app=app)
    # toolbar.init_app(app=app)
    api.init_app(app=app)