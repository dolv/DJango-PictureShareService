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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponseRedirect

from Core import views as core_views

# Страницы
# /
#     главная - форма для загрузки и галерея последних загруженных картинок
# /popular
#     галерея популярных картинок
# /<key>
#    страница отдельной картинки

urlpatterns = [
    url(r'^user/login/$', core_views.LoginView.as_view(), name="login-page"),
    url(r'^user/logout/$', core_views.logoutView, name="logout"),
    url(r'^admin/', admin.site.urls),
    url(r'^popular/$', core_views.PopularView.as_view(), name='popular'),
    url(r'^update/$', core_views.PictureUpdateView.as_view(), name='picture-update'),
    url(r'^$', core_views.PictureUploadView.as_view(), name='home-page'),
    url(r'^([\w\d-]+)$', core_views.PicturePreviewPageView.as_view(), name='picture-details'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
