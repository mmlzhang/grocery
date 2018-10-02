from flask import Blueprint, render_template,\
    make_response, request, session, redirect, url_for

from APP.models import db, Student, User

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/setcookie/')
def set_cookie():
    temp = render_template('cookies.html')
    # 服务端创建响应
    res = make_response(temp)
    # 绑定cookie     set_cookie(key, value, max_age, expires)
    res.set_cookie('ticket', '123123', max_age=10)
    return res


@user_blueprint.route('/delcookie/')
def del_cookie():
    temp = render_template('cookies.html')
    res = make_response(temp)
    res.delete_cookie('ticket')
    return res


@user_blueprint.route('/reg/')
def reg():

    return ''

@user_blueprint.route('/lg/', methods=['GET', 'POST'])
def lg():
    if request.method == 'GET':
        return ''

    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
        return ''


@user_blueprint.route('/scores/', methods=['GET'])
def stu_scores():
    scores = [i * 10 for i in range(1, 8)]
    content_h2 = '<h2>ABC</h2>'
    content_h3 = ' <h2> 空格 </h2> '

    return render_template('scores.html',
                           scores=scores,
                           content_h2=content_h2,
                           content_h3=content_h3)


# 创建数据库 的 表
@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '<h1>创建成功!<h1>'


# 删除 表
@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()  # 删除说有表
    return '删除所有表成功!'


@user_blueprint.route('/create_stu/', methods=['GET', 'POST'])
def create_stu():

    stu = Student()
    stu.s_name = '孙策'
    stu.s_age = '20'

    db.session.add(stu) # 添加数据
    db.session.commit() # 提交数据

    return '创建学生成功'


# 增删改查
@user_blueprint.route('/select_stu/', methods=['GET'])
def select_stu():
    # stus = Student.query.filter(Student.s_name=='孙权') # 查询
    # stus = Student.query.filter_by(s_name='孙权') # 查询
    # 查询所有
    # stu_all = Student.query.all()

    # 更新, 修改
    Student.query.filter(Student.s_name == '孙权').first()

    stu = Student.query.filter_by(s_name='孙权').first()
    stu.s_name = '曹操'
    db.session.add(stu)
    db.session.commit()

    # db.session.delete(stu) # 删除
    # db.session.commit()

    # return render_template('students.html', stus=stus, stu_all=stu_all)
    return '<h1>OK</h1>'



@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        if all([username, password, re_password]):
            if password == re_password:
                user = User()
                user.username = username
                user.password = password
                user.email = email

                db.session.add(user)
                db.session.commit()

                return redirect(url_for('user.login'))
        return render_template('user/register.html')


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user.password == password:
            user.ticket = 'ticket'
            db.session.add(user)
            db.session.commit()

            return '<h2>登录成功!</h2>'

        session['username'] = username
        return render_template('user/login.html', username=username)