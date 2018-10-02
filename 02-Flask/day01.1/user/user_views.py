from flask import Blueprint, render_template, \
                  request, make_response, redirect, \
                  url_for

user_blueprint = Blueprint('user', __name__)  # 相当于 django 的 namespace


@user_blueprint.route('/')
def hello():
    return 'hello'


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        # username = request.form.getlist('username')
        return username


@user_blueprint.route('/response/', methods=['GET', 'POST'])
def rsp():
    res = make_response('<h2>hello</h2>', 200)
    return res


@user_blueprint.route('/redirect/')
def redct():
    return redirect(url_for('user.login'))  # 蓝图的第一个参数 + 加函数名