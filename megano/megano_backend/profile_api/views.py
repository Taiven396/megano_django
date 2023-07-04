from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from .serializers import ProfileSerializer, ProfileAvatarSerializer, PasswordSerializer
from django.contrib.auth import login
from .models import Profile


class ProfileRetrievUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Получает и возвращает Profile пользователя
        """
        return self.request.user.profile
    
    def retrieve(self, request) -> Response:
        """
        Получает Profile пользователя
        """
        try:
            request.session['username'] = request.user.username
            print(request.session['username'])
            print(type(request.session))
            data = self.get_serializer(self.request.user.profile).data
        except Exception:
            return Response(data={})
        return Response(data=data)
    
    def post(self, request, *args, **kwargs):
        """
        Обновляет Profile пользователя
        """
        print(request.data)
        data = request.data
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            return super().update(request, *args, **kwargs)
        print('Не валидный')
        data = {'error': 'Невалидные данные'}
        return Response(status=409, data=data)
    

class ProfileAvatarUpdateView(UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    
    def get_object(self):
        """
        Получает и возвращает Profile пользователя
        """        
        return self.request.user.profile
    
    def post(self, request, *args, **kwargs):
        """
        Обновляет профайл пользователя
        """
        return super().update(request, *args, **kwargs)
    

class PasswordApiView(APIView):
    """
    API представление для изменения пароля пользователя.
    После успешной проверки пользователя через сериализатор, 
    изменяет пароль на новый.
    
    Поля запроса:
    currentPassword: str Текущий пароль пользователя
    newPassword: str Новый паролья пользователя
    
    Возвращает:
    Response(status)
    200: Пароль успешно изменён
    400: Введён неверный текущий пароль
    """
    
    def post(self, request):
        data = request.data
        data['username'] = request.user.username
        print(data)
        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():      
            return Response(status=200)
        return Response(status=400)