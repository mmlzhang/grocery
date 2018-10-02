from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(16),unique=True)
    s_age = db.Column(db.Integer, default=18)
    s_yuwen = db.Column(db.Float)

    __tablename__ = 'tb_student'  # 定义数据库 表 的名称


class User(db.Model):

    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(100))
    ticket = db.Column(db.String(200))

    __tablename__ = 'tb_user'