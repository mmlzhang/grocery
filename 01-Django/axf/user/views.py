from json import dumps

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from datetime import datetime, timedelta

from user.models import UserModel, UserTicketModel
from utils.function import create_ticket


def register(request):
    """
    注册
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')
        # 加密
        password = make_password(password)   # 加密
        if not all([username, password, icon]):
            msg = '不能为空'
            return render(request, 'user/user_register.html',
                          {'msg': msg})
        #创建用户
        user = UserModel(username=username,email=email,
                         password=password, icon=icon)
        if user:
            user.save()
        return HttpResponseRedirect(reverse('axf:mine'))


def checkuser(request):
    """检查是否重名"""
    username = request.GET.get('username')
    user = UserModel.objects.filter(username=username)
    data = {}
    if user:
        data['status'] = 900
        data['desc'] = '用户名已存在'
    else:
        data['status'] = 200
        data['desc'] = ''

    response = HttpResponse(dumps(data))
    return response  # Jsonresponse(data)


def login(request):
    """
    登录
    """
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserModel.objects.filter(username=username).first()
        ticket = create_ticket()
        # 将相应提取出来, 等待绑定 ticket 后返回
        resopnse = HttpResponseRedirect(reverse('axf:mine'))
        # 设置过期时间
        out_time = datetime.now() + timedelta(days=1)
        # 用户是否存在  验证密码
        if user and check_password(password, user.password):
            # 保存 ticket 得到用户, 已近存在于表中就只更新 ticket 和 过期时间
            user_t = UserTicketModel.objects.get_or_create(user_id=user.id)[0] # 得到的是个 tuple 需要取值
            # 数据库保存 用户的 ticket,out_time
            user_t.ticket = ticket
            user_t.out_time = out_time
            user_t.save()
            # 将ticket 绑定在 响应 中
            resopnse.set_cookie('ticket', ticket, expires=out_time)
            return resopnse


def logout(request):
    """
    退出登录
    """
    if request.method == 'GET':
        # 删除 cookies 中的ticket
        response = HttpResponseRedirect(reverse('axf:mine'))
        response.delete_cookie('ticket')
        # 删除 UserTicket 中的 ticket
        return response
