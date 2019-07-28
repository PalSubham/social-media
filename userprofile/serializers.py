from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

# Serializer classes are here

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'timezone', 'avatar', 'birthday',)
        extra_kwargs = {
            'birthday': {'allow_null': False, 'required': True,},
        }
    
    def update(self, instance, validated_data):
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):

    userprofile = UserProfileSerializer(required = True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'userprofile',)
        extra_kwargs = {
            'password': {'write_only': True,},
            'first_name': {'allow_null': False, 'required': True,},
            'last_name': {'allow_null': False, 'required': True,},
        }


    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)

        newuser = self.Meta.model.objects.create_user(**validated_data)
        user = authenticate(self.context['request'], username = username, password = password)

        if not user == None:
            userprofile = user.userprofile
            userprofile.timezone = userprofile_data.get('timezone', None)
            userprofile.birthday = userprofile_data.get('birthday', None)
            userprofile.save()
        else:
            newuser.delete()
            raise serializers.ValidationError("Cannot create account", code='authorization')

        return newuser

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance


class UserSignedInSerializer(serializers.ModelSerializer):

    signed_in = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'signed_in',)
    
    def get_signed_in(self, obj):
        return True


class ProfileSerializer(serializers.Serializer):

    user = UserSerializer()
    followings = UserSerializer(many = True)
    followers = UserSerializer(many = True)
    followings_no = serializers.IntegerField()
    followers_no = serializers.IntegerField()
    total_posts = serializers.IntegerField()


class SignInSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)
    email = serializers.EmailField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if username and password and email:
            user = authenticate(self.context['request'], username = username, password = password)

            if not user:
                raise serializers.ValidationError('Incorrect username or password.', code='authorization')
            if not user.is_active:
                raise serializers.ValidationError('This user is not active.', code='authorization')
            if not user.email == email:
                raise serializers.ValidationError('Incorrect Email ID.', code='authorization')
        else:
            raise serializers.ValidationError('Missing credential(s).', code='authorization')
        
        data['user'] = user

        return data
