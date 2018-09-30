from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from blogMe.settings import MEDIA_ROOT, MEDIA_URL

from blog import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # 首页
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^user/', include('user.urls', namespace='user')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

