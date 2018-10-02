from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
    login_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, username):
        self.username = username

    @property
    def password(self):
        raise AttributeError('禁止直接获取密码!')

    # 保存密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码  正确返回的是True
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %s>' % self.username


class Role(db.Model):
    __tablename__ = 'tb_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


