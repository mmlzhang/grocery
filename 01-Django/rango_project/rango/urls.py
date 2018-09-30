from django.conf.urls import url

from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^all_categories/', views.all_categories, name='all_categories'),
    url(r'^all_pages/', views.all_pages, name='all_pages'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^goto/', views.goto, name='goto'),

    url(r'^post_profile/', views.post_profile, name='post_profile'),  # 无用, 最后转到user中
    url(r'^list_profile/', views.list_profile, name='list_profile'),

]