
""" 状态码 """

OK = 200  # 请求成功
SUCCESS = {'code': OK, 'msg': '请求成功'}

# 用户模块
USER_INFO_NOT_INTACT = {'code': 1004, 'msg': '用户信息不完整'}
USER_PHONENUMBER_NOT_VALID = {'code': 1002, 'msg': '手机号码不正确'}
USER_REGISTER_PASSWORD_ERROR = {'code': 1003, 'msg': '密码不一致'}
USER_REGISTER_PHONE_ALERDY_EXISTS= {'code': 1004, 'msg': '该用户已注册,请直接登录'}
USER_REGISTER_SUCCESS = { 'code': OK, 'msg': '注册成功!'}

# login
USER_NOT_EXISTS = {'code': 1005, 'msg': '该用户不存在, 请先注册'}
USER_LOGIN_PASSWORD_ID_NOT_VALID = {'code': 1006, 'msg': '密码输入错误'}
USER_LOGIN_SECCESS = {'code': OK, 'msg': '登录成功!'}

# 上传文件
USER_PROFILE_ERROR = {'code': 1007, 'msg': '文件格式不正确'}
DATABASE_ERROR = {'code': 1008, 'msg': '数据库错误, 请稍后再试'}

USER_NAME_ALERDY_EXISTS = {'code': 1009, 'msg': '用户名已存在'}
USER_INFO_NAME_CHANGE_SUCCESS = {'code': OK, 'msg': '用户名更换成功'}
USER_NOT_LOGIN = {'code': 1011, 'msg': '用户未登录'}


# 实名认证
USER_AUTH_INFO_NOT_INTACT = {'code': 1012, 'msg': '用户认证信息不完整'}
USER_AUTH_ID_NOT_AVALID = {'code': 1013, 'msg': '身份证号码不正确'}

# 房屋 house



# order
ORDER_DAYS_ERROR = {'code': 1100, 'msg': '订单的结束时间不能小于开始时间'}



