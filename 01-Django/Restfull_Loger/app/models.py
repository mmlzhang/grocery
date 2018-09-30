from django.db import models


class Grade(models.Model):
    g_name = models.CharField(max_length=20)
    g_create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_grade'

    def __str__(self):
        return self.g_name


class Student(models.Model):

    s_name = models.CharField(max_length=20, null=False, unique=False)
    s_sex = models.BooleanField(default=0)
    s_birth = models.DateField(null=True)
    s_delete = models.BooleanField(default=0)
    s_create_time = models.DateTimeField(auto_now_add=True)  # 创建时间不会修改
    s_operate_time = models.DateTimeField(auto_now=True)  # 每次修改时间改变
    s_tel = models.CharField(max_length=11, null=True)
    s_shuxue = models.IntegerField(null=True)
    s_yuwen = models.IntegerField(null=True)
    g = models.ForeignKey(Grade)  #  加 unique=True  一对一
    s_img = models.ImageField(upload_to='upload', null=True)


    def __str__(self):
        return self.s_name

    class Meta:
        db_table = 'tb_student'

    # def __init__(self, s_name, g_id):
    #     self.s_name = s_name
    #     self.g_id = g_id

class StuInfo(models.Model):

    s_addr = models.CharField(max_length=30, null=True)
    s_age = models.IntegerField()
    s = models.OneToOneField(Student)

    class Meta:
        db_table = 'tb_stu_info'


class Card(models.Model):

    cd = models.CharField(max_length=50)
    s = models.ForeignKey(Student)

    class Meta:
        db_table = 'tb_card'



