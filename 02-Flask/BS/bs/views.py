from flask import Blueprint, request, render_template, flash, url_for, redirect

from bs.forms import LoginForm
from bs.models import User

bs = Blueprint('bs', __name__)


@bs.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@bs.route('/head/')
def head():
    return render_template('head.html')


@bs.route('/left/')
def left():
    return render_template('left.html')


@bs.route('/grade/')
def grade():
    return render_template('grade.html')


@bs.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username)
        user.password(password)
        user.save()
        return redirect(url_for('bs.index'))


@bs.route('/login/')
def login():

    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data)
            if user is not None and user.verify_password(form.password.data):
                return '登录成功'

            flash('用户名或密码错误')
        return '登录页面'


