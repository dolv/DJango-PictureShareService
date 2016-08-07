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
from django.conf.urls import url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from Core.views import PictureUploadView, PicturePreviewPageView, PopularView

# Страницы
# /
#     главная - форма для загрузки и галерея последних загруженных картинок
# /popular
#     галерея популярных картинок
# /<key>
#    страница отдельной картинки
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^popular/$', PopularView.as_view(), name='popular'),
    url(r'^$', PictureUploadView.as_view(), name='home-page'),
    url(r'^([\w\d-]+)/$', PicturePreviewPageView.as_view(), name='picture-details'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
