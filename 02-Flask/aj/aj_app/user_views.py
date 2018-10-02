
import re
import os

from flask import Blueprint, render_template, \
    url_for, request, jsonify, session, redirect

from aj_app.models import db, User
from utils import status_code
from utils.decorator import login_required
from utils.settings import BASE_DIR, UPLOAD_DIR


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/tb/')
@login_required
def tb():
    """创建所有 table"""
    db.create_all()
    return 'OK'


@user_blueprint.route('/register/', methods=['GET'])
def register():
    """用户注册   GET 请求"""
    if request.method == 'GET':
        return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    """用户注册   POST 请求"""
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证数据完整性
        if not all([mobile, password, password2]):
            return jsonify(status_code.USER_INFO_NOT_INTACT)
        # 2. 验证手机号码是否真确
        if not re.match(r'^1[34578][0-9]{9}$', mobile):
            return jsonify(status_code.USER_PHONENUMBER_NOT_VALID)
        # 验证密码
        if not password == password2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_ERROR)
        # 保存用户数据
        user = User.query.filter(User.phone==mobile).first()
        if user:
            return jsonify(status_code.USER_REGISTER_PHONE_ALERDY_EXISTS)
        else:
            user = User()
            user.phone = mobile
            user.name = mobile
            user.password = password
            user.add_update()
            return jsonify(status_code.USER_REGISTER_SUCCESS)


@user_blueprint.route('/login/', methods=['GET'])
def login():
    """用户登录   GET 请求"""
    return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    """用户登录   POST 请求"""
    mobile = request.form.get('mobile')
    password = request.form.get('password')

    # 1.验证数据的完整性
    if not all([mobile, password]):
        return jsonify(status_code.USER_INFO_NOT_INTACT)
    # 2. 验证手机正确性
    if not re.match(r'^1[34578][0-9]{9}$', mobile):
        return jsonify(status_code.USER_PHONENUMBER_NOT_VALID)
    # 3. 用户
    user = User.query.filter(User.phone == mobile).first()
    if user:
        if not user.check_password(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_ID_NOT_VALID)
        # 验证通过
        else:
            session['user_id'] = user.id
            return jsonify(status_code.USER_LOGIN_SECCESS)
    else:
        return jsonify(status_code.USER_NOT_EXISTS)


@user_blueprint.route('/logout/', methods=['GET'])
def logout():
    """用户注销   GET 请求"""
    session.clear()
    return redirect(url_for('user.login'))


@user_blueprint.route('/my/', methods=['GET'])
@login_required
def my():
    """个人中心页面   GET 请求"""
    return render_template('my.html')


@user_blueprint.route('/user_info/', methods=['GET'])
def user_info():
    """修改个人信息   GET 请求"""
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    if user:
        data = {
            'name': user.name,
            'phone': user.phone,
            'img_url': '/static/' + user.avatar if user.avatar else '',
        }
        return jsonify({'code': status_code.OK, 'data': data})
    else:
        return jsonify(status_code)


@user_blueprint.route('/profile/', methods=['GET'])
def profile():
    """上传文件   GET 请求"""
    return render_template('profile.html')


@user_blueprint.route('/profile/', methods=['PATCH'])
def user_profile():
    """上传文件 修改用户名   PATCH 请求"""
    file = request.files.get('avatar')
    name = request.form.get('name')
    if file:
        # 校验图片是否格式正确
        if not re.match(r'image/.*', file.mimetype):
            return jsonify(status_code.USER_PROFILE_ERROR) # 图片格式错误
        # 保存图片
        image_path = os.path.join(UPLOAD_DIR, file.filename)
        file.save(image_path)

        user = User.query.get(session['user_id'])
        avatar_path = os.path.join('upload', file.filename)
        user.avatar = avatar_path
        try:
            user.add_update()
        except Exception as e: # 数据库错误
            return jsonify(status_code.DATABASE_ERROR)
        # 上传成功, 将头像信息传回 渲染页面
        return jsonify(code=status_code.OK, img_url='/static/' + avatar_path)
    # 更改姓名
    if name:
        user = User.query.filter(User.name==name).first()
        # 如果有 user 说明用户名重复
        if user:
            return jsonify(status_code.USER_NAME_ALERDY_EXISTS)
        else:
            user = User.query.get(session['user_id'])
            user.name = name
            try:
                user.add_update()
            except Exception as e:
                db.session.rollback()
                return jsonify(status_code.DATABASE_ERROR)
            return jsonify(status_code.USER_INFO_NAME_CHANGE_SUCCESS)


@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    """实名认证  GET"""
    return render_template('auth.html')


@user_blueprint.route('/auth/', methods=['PATCH'])
def user_auth():
    """实名认证  PATCH"""
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')

    if not all([real_name, id_card]):
        return jsonify(status_code.USER_AUTH_INFO_NOT_INTACT) # 信息不能为空

    if not re.match(r'^[1-9]\d{17}', id_card):
        return jsonify(status_code.USER_AUTH_ID_NOT_AVALID)

    user = User.query.get(session['user_id'])
    if user:
        user.id_name = real_name
        user.id_card = id_card
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS)


@user_blueprint.route('/auths/', methods=['GET'])
def user_auths():
    """实名认证信息渲染页面"""
    user = User.query.get(session['user_id'])
    if user:
        real_name = user.id_name
        id_card = user.id_card

        return jsonify(code=status_code.OK, data=user.to_auth_dict())




