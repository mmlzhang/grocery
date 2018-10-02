from flask_session import Session

from aj_app.models import db


se = Session()


def ext_init(app):

    se.init_app(app=app)
    db.init_app(app=app)


