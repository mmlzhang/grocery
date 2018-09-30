from django.conf.urls import url


from blog import views

urlpatterns = [
    url(r'^$', views.base, name='base'), # 首页
    url(r'^article/', views.article, name='article'),
    url(r'^about/', views.about, name='about'),
    url(r'^mood/', views.mood, name='mood'),
    url(r'^article_detail/', views.article_detail, name='article_detail'),
    url(r'^board/', views.board, name='board'),
    url(r'^upload/', views.upload, name='upload'),
]
