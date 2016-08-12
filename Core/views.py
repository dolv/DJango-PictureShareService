from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, ListView, UpdateView, DeleteView, View
from django.forms import formset_factory
from Core import forms as core_forms
from Core import models as core_models
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import auth, messages
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.baseconv import base56
from random import randint
import hashlib

# Create your views here.

# Страницы
# /
#     главная - форма для загрузки и галерея последних загруженных картинок
# /popular
#     галерея популярных картинок
# /<key>
#    страница отдельной картинки

class BaseHeaderMenu(FormView):
    form_class = core_forms.AuthenticationForm()
    ctx = {'login_form': form_class,
           'login_next': ''}


class PictureUploadView(BaseHeaderMenu, FormView):
    parent_class = BaseHeaderMenu
    form_class = core_forms.PictureUploadForm
    model = core_models.Picture
    pictures_in_a_raw = 4
    pictures_to_show = 12
    success_url = 'home-page'
    template_name = "index.html"
    ctx = parent_class.ctx

    def add_queryset_to_ctx(self, ctx):
        queryset = list(self.model.objects.order_by('-uploadTime')[:self.pictures_to_show])
        td_width = 100/self.pictures_in_a_raw - self.pictures_in_a_raw/16
        ctx.update({'queryset': queryset,
                    'td_width': str(td_width)+'%',
                    })

    def gen_random_key(self):
        def get_new_key():
            return base56.encode(randint(0, 0x7fffff))
        key = get_new_key()
        try:
            while self.model.objects.get(key=key):
                key = get_new_key()
        except self.model.DoesNotExist:
            return key

    def get(self, request):
        form = self.form_class(request.GET)
        self.ctx.update({'form': form})
        self.ctx.update({'request': request})
        return render(request, self.template_name, self.ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request.POST.__setitem__('key', self.gen_random_key())
        request.POST.__setitem__('uploadTime', timezone.now())
        request.POST.__setitem__('author', request.user.id)
        form = self.form_class(request.POST, request.FILES)

        # str(hashlib.md5(request.FILES['picture'].file.read()).hexdigest())
        self.ctx.update({'form': form})
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(self.request.POST.get('key'))
        self.add_queryset_to_ctx(self.ctx)
        return render(request, self.template_name, self.ctx)


    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'File uploaded!')
        return super(PictureUploadView, self).form_valid(form)


class PicturePreviewPageView(LoginRequiredMixin, BaseHeaderMenu, DeleteView):
    form_class = core_forms.PictureDetailsForm
    parent_class = BaseHeaderMenu
    template_name = "picture_details.html"
    model = core_models.Picture
    success_url = 'home-page'
    ctx = parent_class.ctx

    def get(self, request, key):
        if request.path == "/favicon.ico/":
            HttpResponseRedirect("/static/favicon.ico")
        instance = self.model.objects.get(key=key)
        instance.viewCounter += 1
        instance.lastViewTime = timezone.now()
        instance.save()
        number_of_likes = core_models.Likes.objects.filter(picture=instance.id, like=1).count()
        number_of_dislikes = core_models.Likes.objects.filter(picture=instance.id, like=0).count()
        try:
            user_like_choice = core_models.Likes.objects.get(picture=instance.id, user=request.user)
        except core_models.Likes.DoesNotExist:
            user_like_choice = None
        if user_like_choice is not None:
            user_like_choice = user_like_choice.like
        form_update = self.form_class()
        form_update.fields['key'].initial = instance.key
        form_update.fields['description'].initial = instance.description
        form_delete = self.form_class()
        like_form = core_forms.LikesForm(initial={'like': True})
        dislike_form = core_forms.LikesForm(initial={'like': False})
        self.ctx.update({'form_update': form_update,
                         'form_delete': form_delete,
                         'instance': instance,
                         'like_form': like_form,
                         'dislike_form': dislike_form,
                         'user_like_choice': user_like_choice,
                         'likes_number': {'positive': number_of_likes,
                                          'negative': number_of_dislikes,
                                          'total': number_of_likes+number_of_dislikes}})
        self.ctx.update({'request': request})

        return render(request, self.template_name, self.ctx)

    def post(self, request, key):
        instance = get_object_or_404(core_models.Picture, key=key)
        instance.delete()
        return HttpResponseRedirect(reverse(self.success_url))


class PictureUpdateView(LoginRequiredMixin, UpdateView):
    form_class = core_forms.PictureDetailsForm
    model = core_models.Picture
    success_url = 'picture-details'

    @method_decorator(login_required)
    def post(self, request):
        instance = get_object_or_404(self.model, key=request.POST.get('key'))
        form = self.form_class(request.POST, instance=instance)
        form.save()
        return HttpResponseRedirect(reverse(self.success_url, args=[instance.key]))


class PopularView(BaseHeaderMenu, ListView):
    parent_class = BaseHeaderMenu
    model = core_models.PictureWithLikesCount
    pictures_in_a_raw = 4
    pictures_to_show = 12
    template_name = "popular.html"
    ctx = parent_class.ctx

    def get(self, request):
        if 'popular' in request.path:
            queryset = list(self.model.objects.order_by('-viewCounter')[:self.pictures_to_show])
            caption = 'The most popular pictures.'
        if 'most-liked' in request.path:
            queryset = list(self.model.objects.order_by('-likes_number')[:self.pictures_to_show])
            caption = 'The most liked pictures.'
        self.ctx.update({'queryset': queryset,
                'td_width': str(100 / self.pictures_in_a_raw - self.pictures_in_a_raw / 16) + '%',
                'caption': caption
                })
        self.ctx.update({'request': request})
        return render(request, self.template_name, self.ctx)


class LoginView(FormView):
    form_class = core_forms.AuthenticationForm
    template_name = 'user_auth/login.html'

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
        return HttpResponseRedirect(request.GET.get('next'))


class LogoutView(FormView):
    template_name = None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponseRedirect(request.GET.get('next'))

class LikesView(View):
    form_class = core_forms.LikesForm
    model = core_models.Likes
    success_url = 'picture-details'

    @method_decorator(login_required)
    def post(self, request, key):
        def str_bool(str_var):
            return {'True': True, 'False': False}[str_var]

        picture = get_object_or_404(core_models.Picture, key=key)
        try:
            like = self.model.objects.get(
                picture=picture,
                user=request.user
            )
            like.like = str_bool(request.POST.get('like'))
            like.created = timezone.now()
            form = self.form_class(request.POST, instance=like)
            if form.is_valid():
                form.save()
        except self.model.DoesNotExist:
            like, created = self.model.objects.get_or_create(picture=picture,
                                                             user=request.user,
                                                             like=str_bool(request.POST.get('like')))
        return HttpResponseRedirect(reverse(self.success_url, args=[key]))