import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse

from user.models import UserTicketModel, UserModel


class UserMiddle(MiddlewareMixin):

    def process_request(self, request):
        # 需要登录  个人中心和购物车
        need_path = ['/user/mine/', ]
        path = request.path
        if path in need_path:
            # 需要先获取 cookies 中的 ticket 参数
            ticket = request.COOKIES.get('ticket')
            if not ticket:
                return HttpResponseRedirect(reverse('user:login'))
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if user_ticket:
                # 获取认证信息, 验证是否过期, 没有过期, request.user 赋值
                #过期 跳转到登录
                if datetime.datetime.now() > user_ticket.out_time.replace(tzinfo=None):
                    # 过期
                    UserTicketModel.objects.filter(user=user_ticket).delete()
                    return HttpResponseRedirect(reverse('user:login'))
                else:
                    # 未过期, 赋值 user   删除多余 ticket 信息
                    request.user = user_ticket.user
                    # 删除多余的认证信息
                    # 查询user  并且 将 ticket中 不等于 cookies 中的 ticket 的记录删除
                    UserTicketModel.objects.filter(
                        Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()
                    return None
            else:
                # ticket 不存在
                return HttpResponseRedirect(reverse('user:login'))

        else:  # path 不再需要验证的路径中 也可以不写
            return None
