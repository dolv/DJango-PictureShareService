"""PictureShareService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from Core import views as core_views

# Страницы
# /
#     главная - форма для загрузки и галерея последних загруженных картинок
# /popular
#     галерея популярных картинок
# /<key>
#    страница отдельной картинки

swagger_view = get_swagger_view(title='Pastebin API')
schema_view = get_schema_view(title='Pastebin API')

router = routers.DefaultRouter()
router.register(r'users', core_views.UserViewSet, base_name='user')
router.register(r'groups', core_views.GroupViewSet)
router.register(r'pictures', core_views.PictureUploadViewSet, base_name='pictures')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^schema/$', schema_view),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^swagger/v1/$', swagger_view),
    url(r'^user/login/$', core_views.LoginView.as_view(), name="login-page"),
    url(r'^user/logout/$', core_views.LogoutView.as_view(), name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^popular/$', core_views.PopularView.as_view(), name='popular'),
    url(r'^most-liked/$', core_views.PopularView.as_view(), name='popular'),
    url(r'^update/$', core_views.PictureUpdateView.as_view(), name='picture-update'),
    url(r'^api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', core_views.PictureUploadView.as_view(), name='home-page'),
    url(r'^([\w\d-]+)/$', core_views.PicturePreviewPageView.as_view(), name='picture-details'),
    url(r'^([\w\d-]+)/like/$', core_views.LikesView.as_view(), name='picture-like'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
