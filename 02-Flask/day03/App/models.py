from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class CeleryTest(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    v1 = db.Column(db.String(20))
    v2 = db.Column(db.String(20))
    v3 = db.Column(db.String(20))
    count = db.Column(db.Integer)

    __tablename__ = 'tb_celery_test'


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


from datetime import datetime

from flask import current_app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature)


# pylint: disable=cyclic-import


class Lazy(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    active = db.Column(db.Boolean, default=True)


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime)
    icon = db.Column(db.String(128))
    lable = db.Column(db.String(45))
    country = db.Column(db.String(16))
    address = db.Column(db.String(128))
    group = db.Column(db.String(12))
    level = db.Column(db.Integer)
    advertiser_id = db.Column(db.Integer)

class Advertiser(db.Model):

    __tablename__ = 'advertiser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    status = db.Column(db.String(16))
    email = db.Column(db.String(64))
    group = db.Column(db.String(16))
    am_id = db.Column(db.String(64))
    create_time = db.Column(db.DateTime)
    last_update_time = db.Column(db.DateTime)

class UserFavoriteTask(db.Model):

    __tablename__ = 'user_favorite_task'
    __table_args__ = (db.PrimaryKeyConstraint('task_id', 'user_id'),)

    def __init__(self, user_id, task_id, status):
        self.user_id = user_id
        self.task_id = task_id
        self.status = status

    task_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())
    status = db.Column(db.String(10))
    create_time = db.Column(db.DateTime)

class CreativeMessage(db.Model):

    __tablename__ = 'creative_message'

    id = db.Column(db.Integer, primary_key=True)
    status_from = db.Column(db.String(10))
    status_to = db.Column(db.String(10))
    message = db.Column(db.String(10))


class Creative(db.Model):

    __tablename__ = 'creative'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16))
    type = db.Column(db.String(24))
    img_url = db.Column(db.String(256))
    video_url = db.Column(db.String(256))
    note = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    ad_hash = db.Column(db.String(64))
    gid = db.Column(db.String(256))
    remarks = db.Column(db.String(64))
    advertiser_id = db.Column(db.Integer)
    operator_id = db.Column(db.Integer)
    status_from = db.Column(db.String(16))
    create_time = db.Column(db.DateTime)
    last_update_time = db.Column(db.DateTime)

class Task(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(16))
    name = db.Column(db.String(64))
    creative_type = db.Column(db.String(8))
    commission_rate = db.Column(db.DECIMAL)
    priority = db.Column(db.Integer)
    category = db.Column(db.String(18))
    platform = db.Column(db.String(16))
    resolution_ids = db.Column(db.String(32))
    advertiser_id = db.Column(db.Integer)
    goal = db.Column(db.String(24))
    need_gid = db.Column(db.Boolean, default=False)
    gender = db.Column(db.String(8))
    age = db.Column(db.String(16))
    landing_page = db.Column(db.String(128))
    country = db.Column(db.String(16))
    ad_account = db.Column(db.String(128))
    submit_window = db.Column(db.Integer)
    language = db.Column(db.String(64))
    # 受众用户 描述
    audience = db.Column(db.Text)
    note = db.Column(db.Text)
    creative_limit = db.Column(db.Integer)
    creative_upload_limit = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    last_update_time = db.Column(db.DateTime)
    submit_time = db.Column(db.DateTime)
    publish_time = db.Column(db.DateTime)



class Resolution(db.Model):

    __tablename__ = 'resolution'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(16))
    creative_type = db.Column(db.String(24))
    desc = db.Column(db.String(128))
    pixel = db.Column(db.String(16))
    resolution = db.Column(db.String(16))
    config = db.Column(db.String(256))


class TaskGoal(db.Model):

    __tablename__ = 'task_goal'

    name = db.Column(db.String(24), primary_key=True)
    description = db.Column(db.String(256))


class TaskCategory(db.Model):

    __tablename__ = 'task_category'

    name = db.Column(db.String(24), primary_key=True)


class CountryLanguage(db.Model):

    __tablename__ = 'country_language'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(12))
    name = db.Column(db.String(64))
    abbreviation = db.Column(db.String(16))


class CreativeDaySummary(db.Model):

    __tablename__ = 'creative_day_summary'

    id = db.Column(db.Integer, primary_key=True)
    creative_id = db.Column(db.Integer)
    imp = db.Column(db.Integer)
    click = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    advertiser_id = db.Column(db.Integer)
    spend = db.Column(db.DECIMAL)
    revenue = db.Column(db.DECIMAL)
    commission_rate = db.Column(db.DECIMAL)
    day = db.Column(db.Date)
    conversion = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    last_update_time = db.Column(db.DateTime)


class CreativeTotalSummary(db.Model):

    __tablename__ = 'creative_total_summary'

    id = db.Column(db.Integer, primary_key=True)
    creative_id = db.Column(db.Integer)
    imp = db.Column(db.Integer)
    click = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    advertiser_id = db.Column(db.Integer)
    spend = db.Column(db.DECIMAL)
    revenue = db.Column(db.DECIMAL)
    conversion = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    last_update_time = db.Column(db.DateTime)

    def __init__(self):
        self.imp = 0
        self.click = 0
        self.commission_rate = 0
        self.spend = 0
        self.revenue = 0
        self.conversion = 0


class LevelCommissionRateTracking(db.Model):

    __tablename__ = 'level_commission_rate_tracking'

    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)
    tracking_type = db.Column(db.String(8))
    target_from = db.Column(db.DECIMAL)
    target_to = db.Column(db.DECIMAL)
    update_time = db.Column(db.DateTime)

    def __init__(self, operator_id, target_id, tracking_type, target_from, target_to):
        self.operator_id = operator_id
        self.target_id = target_id
        self.tracking_type = tracking_type
        self.target_from = target_from
        self.target_to = target_to
        self.update_time = datetime.utcnow()


class UserLevelCommissionRate(db.Model):

    __tablename__ = 'user_level_commission_rate'

    level = db.Column(db.Integer, primary_key=True)
    commission_rate = db.Column(db.DECIMAL)

    def __init__(self, level, commission_rate):
        self.level = level
        self.commission_rate = commission_rate

class UserRole(db.Model):

    __tablename__ = 'user_role'
    __table_args__ = (db.PrimaryKeyConstraint('role_id', 'user_id'),)

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    role_id = db.Column(db.Integer())
    user_id = db.Column(db.Integer())


class RolePermission(db.Model):

    __tablename__ = 'role_permission'
    __table_args__ = (db.PrimaryKeyConstraint('role_id', 'permission_id'),)

    def __init__(self, permission_id, role_id):
        self.permission_id = permission_id
        self.role_id = role_id

    role_id = db.Column(db.Integer())
    permission_id = db.Column(db.Integer())


class Permission(db.Model):

    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    group = db.Column(db.String(16))
    display_name = db.Column(db.String(24))


class AdAccount(db.Model):

    __tablename__ = 'ad_account'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(16))
    advertiser_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    act_id = db.Column(db.String(64))
    status = db.Column(db.String(12))
    create_time = db.Column(db.DateTime)


class AdPlatformAccount(db.Model):

    __tablename__ = 'ad_platform_account'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(16))
    status = db.Column(db.String(16))
    advertiser_id = db.Column(db.Integer)
    token = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime)
    uuid = db.Column(db.String(45))
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
