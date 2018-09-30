import random

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

from user.models import User, Role

from django.contrib.auth.hashers import make_password, check_password


def register(request):
    """注册"""
    if request.method == 'GET':
        return render(request, 'users/registration_form.html')
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        if all([username, password1]):
            if password1 != password2:
                return render(request, 'users/registration_form.html')
            else:
                password = make_password(password1)
                user = User(username=username, email=email, password=password)
                user.save()
                return HttpResponseRedirect(reverse('user:login'))
        # return render(request, 'users/registration_form.html')


def register_complete(request):
    """注册完毕跳转页面, 丢弃不用"""
    if request.method == 'GET':
        return render(request, 'users/registration_complete.html')


def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'users/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        ps = user.password
        ps_checkout = check_password(password, ps)
        if ps_checkout:  # 先产生随机的字符串, 长度 28  绑定在user 和 cookie
            s = 'sadfwiueyiadhfkajrqijfalkjvoiroei12343238'
            ticket = ''
            for i in range(28):
                ticket += random.choice(s)
            user.ticket = ticket  # 保存在数据库
            user.save()
            response = HttpResponseRedirect(reverse('rango:index'))
            response.set_cookie('ticket', ticket)  # 保存在 cookie 中 # max_age=1209600  存活时间
            return response
    return HttpResponseRedirect(reverse('rango:index'))


def logout(request):
    """注销"""
    if request.method == 'GET':
        response = HttpResponseRedirect(reverse('rango:index'))
        response.delete_cookie('ticket')
        return response


def all_users(request):
    """所有用户"""
    if request.method == 'GET':
        page_num = request.GET.get('page_num', 1)
        pages = User.objects.all()
        num = len(pages)
        paginator = Paginator(pages, 5)
        user_list = paginator.page(int(page_num))
        context_dict = {'pages': user_list, 'num': num}
        return render(request, 'users/all_users.html', context_dict)


def edit_user(request):
    """编辑用户"""
    user_id = None
    if request.method == 'GET':
        if 'user_id' in request.GET:
            user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        all_roles = Role.objects.all()
        return render(request, 'users/edit_user.html', {'user':user, 'all_roles': all_roles})

    if request.method == 'POST':
        username = request.POST.get('username') # split() 得到的是一个列表
        role_id = request.POST.get('role_id')
        user = User.objects.filter(username=username).first()
        user.role_id = int(role_id)
        user.save()
        return HttpResponseRedirect(reverse('user:all_users'))


def role_permission(request):
    """角色权限"""
    if request.method == 'GET':
        roles = Role.objects.all()
        return render(request, 'users/role_permission.html', {'roles':roles})