from django.conf.urls import url

from user import views

urlpatterns = [
# 自己实现登录注册
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

    # 权限角色
    url(r'userper/', views.userper, name='userper')
]
"""
# django 自带登录注册  
    url(r'^djregister/', views.register, name='register'),
    url(r'^djlogin/', views.login, name='login'),
    url(r'^djlogout/', views.logout, name='logout'),
"""