from django.contrib.auth.models import User, Group
from .models import Picture
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class PictureListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Picture
        # fields = ('picture', 'description', 'key', 'uploadTime', 'lastViewTime', 'viewCounter', 'author')
        fields = '__all__'
        # read_only_fields = ('picture', 'description', 'key', 'uploadTime', 'lastViewTime', 'viewCounter', 'author')