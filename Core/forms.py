from django import forms
from .models import Picture, Likes
from django.contrib.auth.models import User


class PictureUploadForm(forms.ModelForm):
    """Upload files with this form"""
    picture = forms.ImageField()
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Picture description goes here.'}),
                                  required=False)
    key = forms.SlugField(widget=forms.HiddenInput(),
                          required=False)

    class Meta:
        model = Picture
        fields = ('picture','description','key', 'uploadTime')


class PictureDetailsForm(forms.ModelForm):
    """Show picture details with this form"""

    class Meta:
        model = Picture
        fields = '__all__'


class AuthenticationForm(forms.ModelForm):
    username = forms.TextInput()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
