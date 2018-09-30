from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from user.models import UserTicketModel, UserModel


class UserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        ignore_path = ['/user/login/', '/user/register/']
        if path in ignore_path:
            return None

        ticket = request.COOKIES.get('ticket')  # 拿到 ticket
        if ticket:# 找出用户
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if user_ticket: # 判断是否过期, 没过期绑定 user 在request 中
                if datetime.utcnow() < user_ticket.out_time.replace(tzinfo=None):
                    request.user = user_ticket.user # 绑定 user 在 request 中
