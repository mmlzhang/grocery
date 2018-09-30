from django.db import models


class Users(models.Model):

    username = models.CharField(max_length=10, unique=False)
    password = models.CharField(max_length=100)
    ticket = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'tb_user'


class Permission(models.Model):
    p_name = models.CharField(max_length=15)
    p_en = models.CharField(max_length=15)

    def __str__(self):
        return self.p_name

    class Meta:
        db_table = 'tb_permission'


class Role(models.Model):

    r_name = models.CharField(max_length=15)
    u = models.OneToOneField(Users)  # 一对一  ForeignKey+Unique也是
    r_p = models.ManyToManyField(Permission)  # 角色的权限

    def __str__(self):
        return self.r_name

    class Meta:
        db_table = 'tb_role'