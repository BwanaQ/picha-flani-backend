from django.db.models import fields
from rest_framework import serializers
from .models import Photo
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'photos']

class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Photo
		fields = ('title', 'description','webp_image','image', 'price', 'owner')
