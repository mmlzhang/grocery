# from django.contrib.auth.models import User
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import auth
from user.models import Users, Role, Permission


# """
#     注册
# def register(request):
#     if request.method == "GET":
#         msg = None
#         return render(request, 'register.html', {'msg':msg})
#     if request.method == 'POST':
#         username = request.POST.get('username').strip()
#         psw1 = request.POST.get('password')
#         psw2 = request.POST.get('re_pwd')
#         if not all([username, psw1, psw2]):
#             msg = '用户名或密码不能为空'
#             return render(request, 'register.html', {'msg': msg})
#         elif psw1 != psw2:
#             msg = '两次输入密码不一致'
#             return render(request, 'register.html', {'msg': msg})
#         User.objects.create_user(username=username, password=psw1)
#         return HttpResponseRedirect(reverse('user:login'))
# """
# """
#     登录
# """
# def login(request):
#     if request.method == "GET":
#         return render(request, 'login.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # 返回验证成功的用户信息
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             auth.login(request, user)  # 数据库登录
#             return HttpResponseRedirect(reverse('app:index'))
#         else:
#             msg = '用户名或密码输入错误'
#             return render(request, 'login.html', {'msg':msg})
#
# """
#     注销
# """
# def logout(request):
#     if request.method == "GET":
#         auth.logout(request)
#         return HttpResponseRedirect(reverse('user:login'))



def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == 'POST':
        u_name = request.POST.get('username')
        psw1 = request.POST.get('password')
        psw2 = request.POST.get('re_pwd')
        if not all([u_name, psw1, psw2]):
            msg = '用户名或密码不能为空'
            return render(request, 'register.html', {'msg': msg})
        elif psw1 != psw2:
            msg = '两次输入密码不一致'
            return render(request, 'register.html', {'msg': msg})
        Users.objects.create(username=u_name, password=psw1) # 创建用户
        return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(username=username, password=password).first()
        if user:  # 先产生随机的字符串, 长度 28  绑定在user 和 cookie
            s = 'sadfwiueyiadhfkajrqijfalkjvoiroei12343238'
            ticket = ''
            for i in range(28):
                ticket += random.choice(s)
            user.ticket = ticket  # 保存在数据库
            user.save()
            response = HttpResponseRedirect(reverse('app:index'))
            response.set_cookie('ticket',ticket)# 保存在 cookie 中 # max_age=1209600  存活时间
            return response
        else:
            msg = '用户名或密码错误'
            return render(request, 'login.html', {'msg': msg})



def logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('user:login'))
        response.delete_cookie('ticket')
        return response


def userper(request):
    # 查询妲己有哪些权限
    user = Users.objects.filter(username='妲己').first()
    # roll = Roll.objects.filter(u=user).first()
    u_r_p = user.role.r_p.all()  # 一对一  一对多 加_set
    # 判断妲己是否有学生列表权限
    p = u_r_p.filter(p_en="STUDENTLIST")
    # 通过在role模型中设置的关联, 来调用role模型来查找User
    Users.objects.filter(role__r_name__contains='主')

    pass