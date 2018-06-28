from django import forms
from .models import Picture, Likes
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory

class PictureUploadForm(forms.ModelForm):
    """Upload files with this form"""
    picture = forms.ImageField()
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Picture description goes here.'
            }
        ),
        required=False)
    key = forms.SlugField(
        widget=forms.HiddenInput(),
        required=False)

    class Meta:
        model = Picture
        fields = ('picture','description','key', 'uploadTime','author')


class PictureDetailsForm(forms.ModelForm):
    """Show picture details with this form"""
    description = forms.Textarea(
        attrs={
            'class': 'form-control',
            'align': 'left',
            'style': 'white-space: normal; '
            'text-align: justify;'
        },
    )
    key = forms.SlugField(widget=forms.HiddenInput(),
                          required=False)

    class Meta:
        model = Picture
        fields = ('description','key')


class AuthenticationForm(forms.ModelForm):
    username = forms.TextInput()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class LikesForm(forms.ModelForm):
    like = forms.BooleanField(widget=forms.HiddenInput(),
                              required=False)
    picture = forms.IntegerField(required=False)
    user = forms.IntegerField(required=False)

    class Meta:
        model = Likes
        fields = ('like',)