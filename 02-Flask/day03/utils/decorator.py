from flask import redirect, url_for, session


"""  验证登录的装饰器
"""
def is_login(func):
    def check_login(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return check_login