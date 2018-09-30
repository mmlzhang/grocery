from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

from django.core.urlresolvers import reverse

from app.filters import StudentFilter
from app.models import Grade, Student
from day010.settings import PAGE_NUMBERS   # 在 setttings 中设置分页的条数
from user.models import Users

from utils.functions import is_login

"""
    首页
"""
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

# 无中间键写法
        # ticket = request.COOKIES.get('ticket')
        # user = Users.objects.filter(ticket=ticket)
        # if user:
        #     return render(request, 'index.html')
        # else:
        #     return HttpResponseRedirect(reverse('user:login'))

"""
    头部
"""
def head(request):
    if request.method == 'GET':

        return render(request, 'head.html')

"""
    左边
"""
def left(request):
    if request.method == 'GET':

        return render(request, 'left.html')

"""
    查看年级, 分页显示, 调用 Paginator
"""
# def grade(request):
#
#     if request.method == 'GET':
#         page_num = request.GET.get('page_num', 1)  # 设默认参数, 首次获取得到默认参数
#         grade_list = Grade.objects.all()
#         num = len(grade_list)
#         paginator = Paginator(grade_list, PAGE_NUMBERS)  # 得到一个类似于orderedtuple, 可以通过 下标得到相应的页面内容
#         pages = paginator.page(int(page_num))
#         ctx = {
#             'num': num,
#             # 'grade_list': grade_list,
#             'pages': pages
#         }
#         return render(request, 'grade.html', ctx)
"""
# def addgrade(request):
        添加班级  get_or_create()
#     if request.method == 'POST':
#         grade_name = request.POST['grade_name']   # 查重复
#         Grade.objects.get_or_create(g_name=grade_name)  # 不存在,返回False, 并且创建对象
#     return render(request, 'addgrade.html')
"""

"""
    添加班级
"""
def addgrade(request):

    if request.method == 'POST':
        grade_name = request.POST.get('grade_name')
        #Grade.objects.get_or_create(g_name=grade_name)   #也可以创建, 但是返回的是一个元组
        g = Grade()
        g.g_name = grade_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))
    else:
        return render(request, 'addgrade.html')

"""
    编辑班级
"""
def edit_grade(request):  # 同一页面进行不同的表单提交, 不用写action 默认会提交到 GET过来的路径
    if request.method == 'GET':
        g_id = request.GET.get('g_id')
        return render(request, 'addgrade.html', {"g_id": g_id})
    if request.method == "POST":
        g_id = request.POST.get('g_id')
        g_name = request.POST.get('grade_name')
        g = Grade.objects.filter(pk=g_id).first()
        g.g_name = g_name
        g.save()
        return HttpResponseRedirect(reverse('app:grade'))

"""
对班级进行编辑, 两个页面

def operate_grade(request):
    对班级进行编辑, 两个页面


    if request.method == 'GET':   # 加载页面
        g_id = request.GET.get('g_id')
        g = Grade.objects.filter(pk=g_id).first()
        ctx = {'g': g, 'g_id': g_id}
        return render(request, 'operate_grade.html', ctx)
    else:   # 处理post请求
        g_id = request.POST.get('g_id')
        grade = Grade.objects.filter(pk=g_id).first()
        g_name = request.POST.get('g_name')
        grade.g_name = g_name
        grade.save()
        return HttpResponseRedirect(reverse('app:grade'))
"""

"""
    查看学生
"""
# def student(request):
#     if request.method == 'GET':
#         # student_list = Student.objects.filter(s_delete=False)    # 加按班级分类 order_by('g_id')
#         # num = len(student_list)
#         # page_num = request.GET.get('page_num', 1)
#         # paginator = Paginator(student_list, PAGE_NUMBERS)
#         # pages = paginator.page(int(page_num))
#         # ctx = {
#         #     'num': num,
#         #     'student_list': student_list,
#         #     'pages': pages
#         # }
#         return render(request, 'student.html', ctx)


"""
    增加学生
"""
def addstudent(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        return render(request, 'addstu.html', {'grades':  grades})
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        g_id = request.POST.get('g_id')
        s_img = request.FILES.get('s_img')
        # grade = Grade.objects.filter(id=g_id).first()  #筛选出需要的元素
        # s = Student()
        # s.s_name = student_name
        # s.g = grade
        # s.save()
        s = Student(s_name=student_name, g_id=g_id, s_img=s_img)
        s.save()
        # s = Student(s_name=student_name, g=grade)
        # s.save()
        return HttpResponseRedirect(reverse('app:addstudent'))

"""
    删除学生
"""
def del_student(request):
    if request.method == 'GET':
        stu_id = request.GET.get('stu_id')
        Student.objects.filter(pk=stu_id).delete()
        # try:
        #     stu_id = request.GET.get('stu_id')
        #     Student.objects.get(pk=stu_id).delete()
        # finally:
        return HttpResponseRedirect(reverse('app:student'))


from django.db.models import F, Q
def selectstu(request):

    # 查询班级成绩超过10分的学生
    grade = Grade.objects.filter(id=1).first()
    students = grade.student_set.all()

    # stu = students.filter(s_yuwen__gt=F('s_shuxue')+10)
    stu = students.filter(Q(s_yuwen__gt=80) | Q(s_shuxue__gt=100))

    # s = [stu.s_name]

    return


"""



"""
from app.models import Grade, Student, StuInfo

def select_stuinfo(request):
    #1. 通过某个学生拓展表去获取学生信息
    stu_in_stuinfo = StuInfo.objects.filter(s__s_name='刘备').first() # 得到学生对象
    select_name = stu_in_stuinfo.s.s_name  # 通过关联属性查找另外一张表的属性
    #2. 通过学生表获取个人拓展表的信息
    stu_in_student = Student.objects.filter(s_name='黄忠')
    s = stu_in_stuinfo.s.s_addr

    # 1 通过某个学生拓展表去获取学生信息
    Student.objects.filter(stuinfo__s_addr='成都')
    # 2 通过学生表获取个人拓展表的信息
    stu_in_stuinfo = StuInfo.objects.filter(s__s_name='刘备').first()  # 得到学生对象
    select_name = stu_in_stuinfo.s.s_name  # 通过关联属性查找另外一张表的属性
    # 3. 获取python班下的所有学生的信息和拓展表的信息
    Student.objects.filter(g__g_name='php01班')  # 通过关联属性查找
    # 4. 获取python班下语文成绩大于80分的女学生
    stu = Student.objects.filter(g__g_name='python')
    stu.filter(s_yuwen__gt=80)
    # 5. 获取python班下语文成绩超过数学成绩10分的男学生
    stu.filter(s_yuwen__gte=F('s_shuxue') + 10)
    # 6. 获取出生在80后的男学生，查看他们的班级
    stu = Student.objects.filter(s_birth__year__gte=2000)
    stu.first().g.g_name
    pass


"""
API

rest_framework
"""

from rest_framework import mixins, viewsets
from app.serializer import StudentSerializer, GradeSerializer

"""学生"""
class api_student(mixins.ListModelMixin,      # get
                  mixins.CreateModelMixin,    # post 增加
                  mixins.RetrieveModelMixin,  # 查一个 GET
                  mixins.DestroyModelMixin,  # 删除  DELETE
                  mixins.UpdateModelMixin,   # 修改 PUT(全部) PATCH(部分)
                  viewsets.GenericViewSet):  # 查询

    queryset = Student.objects.filter(s_delete=False)       # 查询学生的所有信息
    serializer_class = StudentSerializer   # 序列化学生的所有信息

    # 过滤
    filter_class = StudentFilter

    #/app/api/student/[id]/   DELETE
    def perform_destroy(self, instance): # 也可以重写方法, 来自定义删除

        instance.s_delete = True
        instance.save()

    # def get_queryset(self):
    #     query =self.queryset
    #     s_name = self.request.query_params.get('s_name')
    #     return query.filter(s_name__contains=s_name)

    # def update(self, request, *args, **kwargs):
    #     pass


"""调用API获取数据, 只返回页面, 数据用Ajax加载"""
def student(request):
    if request.method == "GET":
        return render(request, 'student.html')


class api_grade(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,   # PUT PATCH
                viewsets.GenericViewSet):
    queryset = Grade.objects.all()  # 查询返回的结果
    serializer_class = GradeSerializer


def grade(request):
    if request.method == "GET":
        return render(request, 'grade.html')


def grade_api(request):
    if request.method == 'GET':
        return render(request, 'addgrade.html')


