from django.conf.urls import url

from app import views

from django.contrib.auth.decorators import login_required


# Django 自带验证
# urlpatterns = [
#     url(r'^index/', login_required(views.index), name='index'),
#     url(r'^left/', login_required(views.left), name='left'),
#     url(r'^grade/', login_required(views.grade), name='grade'),
#     url(r'^head/', login_required(views.head), name='head'),
#     url(r'^addgrade/', login_required(views.addgrade), name='addgrade'),
#     url(r'^student/', login_required(views.students), name='student'),
#     url(r'^addstudent/', login_required(views.addstudent), name='addstudent'),
#     url(r'^edit_grade/', login_required(views.edit_grade), name='edit_grade'),  # 一页页面进行编辑操作
#     # url(r'^operate_grade/', views.operate_grade, name='operate_grade'),  # 两个页面操作
#     # url(r'^del_grade/', views.operate_grade, name='del_grade'),
#     url(r'^del_student/', login_required(views.del_student), name='del_student'),
#
# ]

from rest_framework.routers import SimpleRouter
router = SimpleRouter()   # 定义路由
router.register(r'api/student', views.api_student) # 注册
router.register(r'api/grade', views.api_grade)

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^left/', views.left, name='left'),
    url(r'^grade/', views.grade, name='grade'),
    url(r'^head/', views.head, name='head'),
    url(r'^addgrade/', views.addgrade, name='addgrade'),
    url(r'^student/', views.student, name='student'),
    url(r'^addstudent/', views.addstudent, name='addstudent'),
    url(r'^edit_grade/', views.edit_grade, name='edit_grade'),  # 一页页面进行编辑操作
    # url(r'^operate_grade/', views.operate_grade, name='operate_grade'),  # 两个页面操作
    # url(r'^del_grade/', views.operate_grade, name='del_grade'),
    url(r'^del_student/', views.del_student, name='del_student'),

    # F/Q
    url(r'^selectstu/', views.selectstu, name='selectstu'),
    url(r'^select_stuinfo/', views.select_stuinfo, name='select_stuinfo'),

    # api 编辑班级
    url(r'^grade_api/', views.grade_api),
]
urlpatterns += router.urls   #  添加  访问生效