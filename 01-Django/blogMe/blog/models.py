from django.db import models
from django.template.defaultfilters import slugify
from user.models import User


class Category(models.Model):
    """分类"""
    name = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = 'tb_categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章"""
    title = models.CharField(max_length=200)
    introduction = models.CharField(max_length=1000)
    write_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        db_table = 'tb_article'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """评论"""
    user = models.ForeignKey(User)
    content = models.CharField(max_length=2000)
    write_time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0) # 点赞

    class Meta:
        db_table = 'tb_comment'

    def __str__(self):
        return self.user.username
