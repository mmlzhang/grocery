
from django.shortcuts import render, HttpResponseRedirect

from django.core.urlresolvers import reverse

from user.models import Users

from rest_framework.renderers import JSONRenderer

def is_login(func):
    """
    验证是否登录的装饰器

    :param func:
    :return: 验证通过后的执行函数
    """
    def wrapper(request):
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket)
        if not user:
            return HttpResponseRedirect(reverse('user:login'))
        return func(request)
    return wrapper


"""
    重构数据结构, 重写render函数
"""
class CustomJsonRenderer(JSONRenderer):  # 定义后, 在setttings添加
    """
    返回结构重构

    {
        'data': {results},
        'code': 200,
        'msg': 提示信息,
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context: # 判断是否有, render, 有就重构, 没有调用父类
            if isinstance(data, dict):
                code = data.pop('code', 0)
                msg = data.pop('msg', '请求成功')
            else:   # 当不是字典时, 自动绑定参数
                code = 0
                msg = '请求成功'
            res = {
                'code': code,
                'msg': msg,
                'data': data,
            }
            return super().render(res, accepted_media_type, renderer_context)
        else:
            super().render(data, accepted_media_type, renderer_context)