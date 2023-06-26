from rest_framework import serializers
from .models import Profile
from django.contrib.auth import authenticate, login
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
    