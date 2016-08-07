from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View, FormView, ListView, DetailView
from .forms import PictureUploadForm, PictureDetailsForm, AuthenticationForm
from .models import Picture, Likes
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


class PictureUploadView(FormView):
    form_class = PictureUploadForm
    model = Picture
    pictures_in_a_raw = 4
    pictures_to_show = 12
    success_url = 'home-page'
    template_name = "index.html"

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
        ctx = {'form': form}
        self.add_queryset_to_ctx(ctx)
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request.POST.__setitem__('key', self.gen_random_key())
        request.POST.__setitem__('uploadTime', timezone.now())
        form = self.form_class(request.POST, request.FILES)

        # str(hashlib.md5(request.FILES['picture'].file.read()).hexdigest())
        ctx = {'form': form}
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse(self.success_url))
        self.add_queryset_to_ctx(ctx)
        return render(request, self.template_name, ctx)


    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'File uploaded!')
        return super(PictureUploadView, self).form_valid(form)


class PicturePreviewPageView(LoginRequiredMixin, DetailView):
    form_class = PictureDetailsForm
    template_name = "picture_details.html"
    model = Picture

    def get(self, request, key):
        form = self.form_class(request.GET)
        instance = Picture.objects.get(key=key)
        instance.viewCounter += 1
        instance.lastViewTime = timezone.now()
        instance.save()
        ctx = {'form': form,
               'instance': instance}
        return render(request, self.template_name, ctx)


class PopularView(ListView):
    model = Picture
    pictures_in_a_raw = 4
    pictures_to_show = 12
    template_name = "popular.html"

    def get(self, request):
        if request.url ==  "/static/favicon.ico/":
            HttpResponseRedirect("/static/favicon.ico")
        queryset = list(self.model.objects.order_by('-viewCounter')[:self.pictures_to_show])
        ctx = ({'queryset': queryset,
               'td_width': str(100 / self.pictures_in_a_raw - self.pictures_in_a_raw / 16) + '%'
              })
        return render(request, self.template_name, ctx)


class LoginView(FormView):
    form_class = AuthenticationForm
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
        return HttpResponseRedirect(request.GET.get('next', '/'))


def logoutView(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/');