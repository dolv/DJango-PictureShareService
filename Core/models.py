from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.baseconv import base56
from random import randint
from django.conf import settings

# Create your models here.

# Требования к модели для хранения картинки
#
# Поля
# - картинка (ImageField)
# - описание (текстовое поле, опционально)
# - ключ (SlugField, должен быть уникальным)
# - дата/время загрузки
# - дата/время последнего просмотра
# - счетчик просмотров
#
# Методы, которые необходимо реализовать
# - get_absolute_url


class Picture(models.Model):
    picture = models.ImageField(upload_to='media_dir/%Y/%m/%d/%S')
    description = models.CharField(max_length=50, blank=True)
    key = models.SlugField(max_length=4,
                           unique=True,
                           null=False,
                           default=base56.encode(randint(0, 0x7fffff)))
    uploadTime = models.DateTimeField(default=timezone.now())
    lastViewTime = models.DateTimeField(null=True)
    viewCounter = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-uploadTime"]

    def __str__(self):
        return "{}: {}".format(self.key, self.picture)

    def get_absolute_url(self):
        return reverse('key', kwargs={'pk': self.pk})

class Likes(models.Model):
    picture = models.ForeignKey('Picture', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)