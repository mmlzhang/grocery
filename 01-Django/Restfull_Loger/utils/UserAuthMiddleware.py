from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from django.core.urlresolvers import reverse

from user.models import Users

import re

import logging
import django.utils.log
import logging.handlers

logger = logging.getLogger('django.request')  # 日志


# 验证cookie 中的ticket 验证不过, 跳转登录
        # 验证通过, request.user 当前登录用户信息
        # return None 或不 return


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        ignore_path = ['/user/login/', '/user/register/', '/app/api/.*']
        for p in ignore_path:    # 可以优化
            if re.match(p, path): # # 忽略的请求 避免重定向次数过多
                return None
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            logger.error('错误了!!!')
            return HttpResponseRedirect(reverse('user:login'))
        user = Users.objects.filter(ticket=ticket).first()
        if not user:
            request.user = user
        logger.info('%s登录成功!' % user.username)
        request.user = user