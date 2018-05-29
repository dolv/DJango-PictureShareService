from django.db import models
from django.utils import timezone
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.utils.baseconv import base56
from random import randint
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Picture(models.Model):
    picture = models.ImageField(upload_to='media_dir/%Y/%m/%d/%S')
    description = models.CharField(max_length=50, blank=True)
    key = models.SlugField(max_length=4,
                           unique=True,
                           null=False)
    uploadTime = models.DateTimeField(default=timezone.now)
    lastViewTime = models.DateTimeField(null=True)
    viewCounter = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-uploadTime"]

    def __str__(self):
        return "{}: {}".format(self.key, self.picture)

    def get_absolute_url(self):
        return reverse('key', kwargs={'pk': self.pk})

class Likes(models.Model):
    picture = models.ForeignKey('Picture', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField()

    def __str__(self):
        from pprint import pprint
        return str(vars(self))

class PictureWithLikesCount(models.Model):
    picture = models.ImageField(upload_to='media_dir/%Y/%m/%d/%S')
    description = models.CharField(max_length=50, blank=True)
    key = models.SlugField(max_length=4,
                           unique=True,
                           null=False)
    uploadTime = models.DateTimeField(default=timezone.now)
    lastViewTime = models.DateTimeField(null=True)
    viewCounter = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    like_count = models.IntegerField()
    dislike_count = models.IntegerField()
    likes_number = models.IntegerField()

    class Meta:
        db_table = 'PictureWithLikesCount'
        managed = False

