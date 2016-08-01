from django import forms
from .models import Picture, Likes


class PictureUploadForm(forms.ModelForm):
    """Upload files with this form"""
    picture = forms.ImageField()
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Picture description goes here.'}),
                                  required=False)
    key = forms.SlugField(widget = forms.HiddenInput(),
                          required = False)

    class Meta:
        model = Picture
        fields = ('picture','description','key')



class PictureDetailsForm(forms.ModelForm):
    """Show picture details with this form"""

    class Meta:
        model = Picture
        fields = '__all__'
