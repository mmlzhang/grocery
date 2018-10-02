from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Student(db.Model):
    """
     many 的一方, 建立外键
    """
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(20))
    s_age = db.Column(db.Integer, default=20)
    #  表名                                       表名     id
    grades = db.Column(db.Integer, db.ForeignKey('tb_grade.g_id'), nullable=True)

    __tablename__ = 'tb_student'

    def __init__(self, name, age):
        self.s_name = name
        self.s_age = age

    def __repr__(self):
        return '<Student %s>' % self.s_name


class Grade(db.Model):
    """
    one 的一方, 建立连接,反向解析
    """
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(16), unique=True, nullable=True)
    g_desc = db.Column(db.String(30), nullable=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now())
    # 模型名称  backref 自定义 many 与 one 的关联   反向解析名称 数据库中没有此列, 只是方便查询
    students = db.relationship('Student', backref='gde', lazy='dynamic') # dynamic 返回 query 对象

    __tablename__ = 'tb_grade'

    def __str__(self):
        return '<Grade %s>' % self.g_name


# 中间表
sc = db.Table('sc',
            db.Column('s_id', db.Integer, db.ForeignKey('tb_student.s_id'), primary_key=True),
            db.Column('c_id', db.Integer, db.ForeignKey('tb_course.c_id'), primary_key=True),
)


class Course(db.Model):
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(16), unique=True)
    c_create_time = db.Column(db.DateTime, default=datetime.now())
    # 多对多关联关系
    students = db.relationship('Student', secondary=sc,
                               backref='course', lazy=True)

    __tablename__ = 'tb_course'

    def __init__(self, c_id, c_name):
        self.c_id = c_id
        self.c_name = c_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'c_create_time': self.c_create_time.strftime('%Y-%m-%d %H:%m:%S'),
            'students': {stu.s_id: stu.s_name for stu in self.students}
        }

    def __repr__(self):
        return '<Course %s>' % self.c_id


"""登录注册  用户
"""
from flask_login import UserMixin


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    crate_time = db.Column(db.DateTime, default=datetime.now())

    __tablename__ = 'tb_user'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<User %s>" % self.username
