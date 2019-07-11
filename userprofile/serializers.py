from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

# Serializer classes are here

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'timezone', 'avatar', 'birthday',)
    
    def update(self, instance, validated_data):
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):

    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'userprofile',) 

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        user = User.objects.create_user(**validated_data)

        userprofile = UserProfile(owner = user, **userprofile_data)
        userprofile.save()

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance
    