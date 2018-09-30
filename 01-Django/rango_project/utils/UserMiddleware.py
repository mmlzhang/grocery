from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from user.models import User


class UserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        path = request.path
        ignore_path = ['/rango/','/rango/index/', '/rango/about/','/user/login/',
                       '/user/register/', '/user/logout/']
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            if path in ignore_path:
                return None
            return HttpResponseRedirect(reverse('rango:index'))
        user = User.objects.filter(ticket=ticket).first()
        if not user:
            request.user = None
            return HttpResponseRedirect(reverse('rango:index'))
        request.user = user

