from django.db import models



class UserModel(models.Model):
    """用户"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False) # False 女 True 男
    icon = models.ImageField(upload_to='icons')  # 头像
    is_delete = models.BooleanField(default=False) # False 未删除, True 删除

    class Meta:
        db_table = 'axf_users'

    def __str__(self):
        return self.username


class UserTicketModel(models.Model):
    """用户 ticket"""
    user = models.ForeignKey(UserModel) # 关联用户
    ticket = models.CharField(max_length=256) # 密码
    out_time = models.DateTimeField() # 过期时间

    class Meta:
        db_table = 'axf_users_ticket'

    def __str__(self):
        return self.user.username
