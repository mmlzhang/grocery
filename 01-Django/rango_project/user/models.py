from django.db import models


class Permission(models.Model):
    p_hans = models.CharField(max_length=20)
    p_en = models.CharField(max_length=20)

    class Meta:
        db_table = 'tb_permission'

    def __str__(self):
        return self.p_hans


class Role(models.Model):
    name = models.CharField(max_length=15)
    name_en = models.CharField(max_length=20,null=True)
    perms_of_role = models.ManyToManyField(Permission)

    class Meta:
        db_table = 'tb_role'

    def __str__(self):
        return self.name



class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    tel = models.CharField(max_length=11, default=123456789)
    ticket = models.CharField(max_length=50, null=True, )
    create_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now=True)
    login = models.BooleanField(default=0)
    delete = models.BooleanField(default=0)
    role = models.ForeignKey(Role, default=3)
    # is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(null=True)
    picture = models.ImageField(upload_to='profile_image')

    class Meta:
        db_table = 'tb_u_profile'

    def __str__(self):
        return self.user.username + '-tb_u_profile'




