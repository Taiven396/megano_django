from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.response import Response
from django.contrib.auth import authenticate
import datetime
import logging


logger_info = logging.getLogger('info_log')


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']

    def get_avatar(self, obj):
        if obj.avatar:
            return {
                'src': obj.avatar.url,
                'alt': obj.avatar.name
            }
        return None


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar']


class PasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    newPassword = serializers.CharField()
    currentPassword = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        old_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        user = authenticate(username=username, password=old_password)
        print(user)
        if user is None:
            raise serializers.ValidationError()
        user.set_password(new_password)
        logger_info.info(f'Пользователь {user.username} успешно сменил пароль.')
        user.save()
        return data

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        name = validated_data['first_name']
        try:
            User.objects.get(
                username=username
            )
            return False
        except User.DoesNotExist:
            user = User.objects.create(
                username=username,
                first_name=name,
            )
            user.set_password(password)
            user.save()
            logger_info.info(f'Пользователь {user.username} успешно зарегестрировался в системе.')
            Profile.objects.create(
                user=user
                )
            return user


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is None:
            raise serializers.ValidationError()
        logger_info.info(f'Пользователь {user.username} успешно зашёл в систему. {datetime.datetime.now()}')
        return data

