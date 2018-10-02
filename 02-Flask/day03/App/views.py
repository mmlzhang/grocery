import datetime
import random

from flask import Blueprint, render_template, request, \
    redirect, url_for, session, flash

from App.models import db, Student, Grade, Course, User
from utils.decorator import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def index():

    return render_template('base.html')

"""  创建数据库的表
"""
@user_blueprint.route('/create_all/')
def create_db():
    db.create_all()
    return '<h2>Aleady Create_table</h2>'


"""  删除所有表格
"""
@user_blueprint.route('/drop_all/')
def drop_db():
    db.drop_all()
    return '<h2>Aleady Drop_tb </h2>'


"""   创建单个
"""
@user_blueprint.route('/create_stu/', methods=['GET', 'POST'])
def create_stu():
    if request.method == 'GET':
        return render_template('create_stu.html')

    if request.method == 'POST':
        stu_name = request.form.get('stu_name')
        stu_age = request.form.get('stu_age')
        stu = Student()
        stu.s_name = stu_name
        stu.s_age = stu_age
        db.session.add(stu)
        db.session.commit()

        return '创建学生成功!'


""" 批量创建 学生
"""
@user_blueprint.route('/create_stus/', methods=['GET', 'POST'])
def create_stus():
    if request.method == 'GET':
        stu_dict = {
            '华佗': 8001,
            '刘备': 8002,
            '孙权': 8003,
            '孙策': 8004,
            '曹操': 8005,
            '曹丕': 8006,
        }
        stu_list = []
        for i in range(1, 8):
            # stu = Student()
            # stu.s_name = '孙%s' % random.randrange(1000)
            # stu.s_age = '%s' % random.randrange(15, 25)
            # 初始化创建, 在models 中设置 __init__() 方法
            stu = Student('孙%s' % random.randrange(1000),
                          '%s' % random.randrange(15, 25))
            stu_list.append(stu)
        # 批量创建  add_all()
        db.session.add_all(stu_list)
        db.session.commit()
        return '<h2>批量添加成功</h2>'


"""操作, 编辑
"""
@user_blueprint.route('/update_stu/', methods=['GET', 'POST'])
def update_stu():
    if request.method == 'GET':
        s_id = request.args.get('id')
        stu = Student.query.filter(Student.s_id == s_id).first()
        courses = Course.query.all()
        return render_template('stu_edit.html', stu=stu, courses=courses)

    if request.method == 'POST': # 修改学生信息
        s_id = request.form.get('s_id')
        stu_name = request.form.get('stu_name')
        stu_age = request.form.get('stu_age')

        stu = Student.query.filter_by(s_id=s_id).first()
        stu.s_name = stu_name
        stu.s_age = stu_age
        # 更新不必要
        db.session.add(stu)  # 可写可不写

        c_id = request.form.get('course_id')

        course = Course.query.get(c_id)
        course.students.append(stu)  # 添加学生

        db.session.add(course)
        db.session.commit()

        return redirect(url_for('user.stu_list'))


@user_blueprint.route('/stu_list/')
def stu_list():
    """
    所有学生显示
    """

    # stu_all = Student.query.all()

    # sql 查询
    sql = 'select * from tb_student'
    stu_all = db.session.execute(sql)

    return render_template('students.html', stu_all=stu_all)


"""  查询
"""
@user_blueprint.route('/stu_in/', methods=['GET'])
def stu_in():
    stu_list = Student.query.filter(Student.s_id.in_([2, 3, 4, 5, 8, 10]))
    # stu_list = Student.query.filter(Student.s_age.__ge__(20))
    # stu_list = Student.query.filter(Student.s_age >= 20)
    # stu_list = Student.query.filter(Student.s_name.like('刘'))
    stu_list = Student.query.filter(Student.s_name.like('%备%'))
    # stu_list = Student.query.filter(Student.s_name.endswith('备')) # startswith()
    # stu_list = Student.query.filter(Student.s_name.contains('孙'))
    s = Student
    sqf = Student.query.filter

    stu_list = sqf(s.s_age.__le__(20))
    stu_list = sqf(s.s_name.endswith('9'))
    stu_list = sqf(s.s_id == 5).all()
    # stu_list = Student.query.get(5) # 根据主键拿到一个
    # 模糊搜索
    # select * from tb_student where s_name like '%刘备%'
    stu_list = sqf(s.s_name.like('%孙权%'))

    # 筛选  limit  offset order-by('-id')
    stu_list = Student.query.limit(5)  # 得到前5个
    stu_list = Student.query.order_by('s_id').offset(3) # 跳过前三个,获取其他的
    stu_list = Student.query.order_by('s_id').offset(3).limit(5)

    # paginate(分页)  得到的是一个 pagination对象 通过 items 得到所有的内容
    stu_list = Student.query.paginate(1, 10).items # 1页码, 10 条数

    stus = Student.query.paginate(1, 10)
    paginate = stus.items
    # 逻辑运算 and_ or_ not_

    return render_template('students.html', stu_all=stu_list,
                           stus=stus, paginate=paginate)


"""  分页 
"""
@user_blueprint.route('/paginate/', methods=['GET'])
def stu_paginate():
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = 10
        paginate = Student.query.order_by('s_id').paginate(page, page_num)
        stus = paginate.items

        return render_template('stu_paginate.html', stus=stus,
                               paginate=paginate)


@user_blueprint.route('/create_grade/')
def grade():
    grade_list = []
    for i in range(1, 11):
        g = Grade()
        g.g_name = 'pyhton%02d班' % i
        # random.sample(s, num)  随机取样, 得到的是列表
        g.g_desc = random.choice('sadfsadfasfdfsafdasdfweadfadf')
        g.g_create_time = datetime.datetime.now() + datetime.timedelta(hours=i)
        grade_list.append(g)

    db.session.add_all(grade_list)
    db.session.commit()

    return '<h1>创建班级成功</h1>'


"""  显示 班级列表
"""
@user_blueprint.route('/grade_all/')
@is_login
def grade_all():
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)


"""  添加学生
"""
@user_blueprint.route('/create_stu_by_grade/', methods=['GET', 'POST'])
def create_stu_by_grade():

    if request.method == 'GET':
        g_id = request.args.get('g_id')
        return render_template('create_stu.html', g_id=g_id)

    if request.method == 'POST':
        g_id = request.form.get('g_id')
        stu_name = request.form.get('stu_name')
        stu_age = request.form.get('stu_age')
        stu = Student(stu_name, stu_age)
        # stu.s_name = stu_name
        # stu.s_age = stu_age
        stu.grades = g_id
        db.session.add(stu)
        db.session.commit()

        return redirect(url_for('user.grade_all'))


"""   查看学生
"""
@user_blueprint.route('/select_stu_by_grade/', methods=['GET'])
def select_stu_by_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        g = Grade.query.get(g_id)
        stus = g.students

        return render_template('students.html', stu_all=stus, g=g)


""" 添加课程
"""
@user_blueprint.route('/create_course/')
def add_course():
    course_name = {
        'pyhton': 1001,
        'java': 1002,
        '高等数学': 1003,
        '线性代数': 1004,
        '微积分': 1005,
        '政治': 1006,
        '毛泽东思想': 1007
    }
    c_list = []
    for c_name, c_id in course_name.items():
        c = Course()
        c.c_name = c_name
        c.c_id = c_id
        c_list.append(c)
    db.session.add_all(c_list)
    db.session.commit()

    return '<h1>课程添加</h1>'


"""  显示所有课程
"""
@user_blueprint.route('/course_all/')
def course_all():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)


""" 该课程 选课学生列表
"""
@user_blueprint.route('/stu_in_course/', methods=['GET'])
def stu_in_course():
    c_id = request.args.get('c_id')
    course = Course.query.get(c_id)
    stu_list = course.students

    return render_template('students.html', stu_all=stu_list, c=course)


"""  添加课程
"""
@user_blueprint.route('/add_course/', methods=['GET', 'POST'])
def cou():
    if request.method == 'GET':
        courses = Course.query.all()
        return render_template('add_course.html', courses=courses)
    if request.method == 'POST':
        s_id = request.args.get('s_id')
        c_id = request.form.get('course_id')
        stu = Student.query.get(s_id)
        course = Course.query.get(c_id)
        course.students.append(stu)  # 添加学生
        db.session.add(course)
        db.session.commit()

        return redirect(url_for('user.course_all'))


"""   查看学生选课
"""
@user_blueprint.route('/show_course/<int:s_id>/', methods=['GET'])
def show_course(s_id):
    if request.method == 'GET':
        stu = Student.query.get(s_id)
        courses = stu.course
        return render_template('courses.html', courses=courses, stu=stu)


"""  删除课程
"""
@user_blueprint.route('/stu/<int:s_id>/del_course/<int:c_id>/', methods=['GET'])
def del_course(s_id, c_id):
    if request.method == 'GET':
        stu = Student.query.get(s_id)
        course = Course.query.get(c_id)
        course.students.remove(stu)  # 删除该课程的选课学生
        db.session.commit()

        return redirect(url_for('user.stu_in'))


"""   登录 注册
"""
from werkzeug.security import generate_password_hash, check_password_hash


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        flag = True
        if not all([username, password, re_password]):
            msg = '请填写完整信息'
            flag = False
        if len(username) > 16:
            msg = '用户名太长'
            flag = False
        if not flag:
            return render_template('user/register.html', msg=msg)
        else:
            password = generate_password_hash(password)
            user = User(username, password)
            user.save()
            return redirect(url_for('user.login'))


@user_blueprint.route('/login/', methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            msg = '请填写完整登录信息'
            return render_template('user/login.html', msg=msg)
        user = User.query.filter_by(username=username).first()
        # user = User.query.filter(User.username==username).first()
        password_hash = user.password
        if user:
            if check_password_hash(password_hash, password):
                session['user_id'] = user.id  # 写入session
                flash('登录成功!')
                return redirect(url_for('user.course_all'))
        else:
            msg = '用户名或者密码错误'
            return render_template('user/login.html', msg=msg)


@user_blueprint.route('/logout/')
def logout():
    # session.pop('user_id')
    session.clear()
    return redirect(url_for('user.index'))


"""
        API
"""

from flask_restful import Resource
from utils.ext_app import api


class CourseApi(Resource):

    def get(self):
        courses = Course.query.all()

        # course_dict = {}
        # for course in courses:
        #     course_dict[course.c_id] = course.c_name

        data = [course.to_dict() for course in courses]

        # 返回 Json 格式
        return {
            'code': 200,
            'msg': '请求成功',
            'data': data,
        }

    def post(self):
        c_id = request.form.get('c_id')
        c_name = request.form.get('c_name')
        course = Course(c_id, c_name)
        course.save()
        return {
            'code': 200,
            'msg': '创建成功',
            'data': {c_id: c_name}
        }

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()

        return {
            'code': 200,
            'msg': '删除成功',
            'data': {course.c_id: course.c_name}
        }


api.add_resource(CourseApi, '/api/course/', '/api/course/<int:id>/')
