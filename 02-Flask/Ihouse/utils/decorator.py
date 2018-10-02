
from flask import redirect, url_for, session

from functools import wraps


def login_required(func):
    """
    用于登录验证的装饰器

    """
    @wraps(func)   # 修饰 防止函数名冲突
    def check_login(*args, **kwargs):
        # 验证登录
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            # 验证失败 跳转到登录页面
            return redirect(url_for('user.login'))
    return check_login
