from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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

    '''def create(self, validated_data):
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

        return instance'''


class OnlyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name',)


class ProfileSerializer(serializers.Serializer):

    user = UserSerializer()
    followings = UserSerializer(many = True)
    followers = UserSerializer(many = True)
    followings_no = serializers.IntegerField()
    followers_no = serializers.IntegerField()
    total_posts = serializers.IntegerField()


class SignInSerializer(serializers.Serializer):

    username = serializers.CharField(label = 'Username')
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)
    email = serializers.EmailField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if username and password and email:
            user = authenticate(self.context['request'], username = username, password = password)

            if not user:
                raise serializers.ValidationError("Username or Password is incorrect", code='authorization')
            if not user.is_active:
                raise serializers.ValidationError('This user is not active', code='authorization')
            if not user.email == email:
                raise serializers.ValidationError('Incorrect Email ID', code='authorization')
        else:
            raise serializers.ValidationError('Missing credential(s)', code='authorization')
        
        data['user'] = user

        return data
