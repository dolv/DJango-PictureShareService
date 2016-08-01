from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, ListView
from .forms import PictureUploadForm, PictureDetailsForm
from .models import Picture, Likes
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.baseconv import base56
from random import randint

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
    context_object_name = "files"
    success_url = 'home-page'
    template_name = "index.html"
    img_thumbnail = {'height': 300,
                     'width': 300}

    def add_queryset_to_ctx(self, ctx):
        queryset = list(self.model.objects.order_by('-uploadTime')[:self.pictures_to_show])
        extended_queryset = []
        for item in queryset:
            if item.picture.height >= self.img_thumbnail['height']:
                scale = self.img_thumbnail['height'] * 100 / item.picture.height
            else:
                scale = self.img_thumbnail['width'] * 100 / item.picture.width
            size = {'height': item.picture.width * scale,
                    'width': item.picture.width * scale
                    }
            extended_queryset.append({'picture': item,
                                      'size': size})
        queryset = [extended_queryset[x:x + self.pictures_in_a_raw] for x in
                    range(0, len(extended_queryset), self.pictures_in_a_raw)]
        ctx.update({'queryset': queryset,
                    'td_width': str(100/self.pictures_in_a_raw)+'%'
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

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.key = self.gen_random_key()
        ctx = {'form': form}
        if form.is_valid():
            form.save(commit=True)
            print(reverse(self.success_url))
            return HttpResponseRedirect(reverse(self.success_url))
        self.add_queryset_to_ctx(ctx)
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'File uploaded!')
        return super(PictureUploadView, self).form_valid(form)

class PicturePreviewPageView(FormView):
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