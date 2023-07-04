from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from profile_api.models import Profile
from orders_api.models import Order
from .serializers import UserSerializer, LogInSerializer
from typing import Dict, List
import datetime
import logging
import json


logger_info = logging.getLogger('info_log')


class SignInApiView(APIView):
    """
    API представление для входа в систему.
    Принимает POST запрос с данными пользователя:
    (username, password). Проверяет данные с помощью
    сериализатора, при успешной проверке,
    выполняет вход (login).
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data['username'])
            serialize = LogInSerializer(data=data)
            if serialize.is_valid():
                print('asd')
                login(user=user, request=request)
                if request.session.get('orderId'):
                    order = Order.objects.get(id=request.session['orderId'])
                    order.customer = user
                    order.save()
                return Response(status=200)
        except:
            return Response(status=409)
    

class SignOutApi(APIView):
    """
    API представление для выхода из системы.
    Принимает POST запрос для выхода из системы.
    Выполняет (logout).
    """
    
    def post(self, request):
        logger_info.info(f'Пользователь {request.user.username} успешно'
                         f'вышел из системы. {datetime.datetime.now()}')
        logout(
            request=request
        )
        return Response(status=200)
        
        
class SignUpCreateApiView(CreateAPIView):
    """
    ApiView представление принимает
    данные из запроса, проверяет валидность
    и уникальность username, если проверка успешна
    создает нового User (регестрирует) и выполняет
    login
    """
    serializer_class = UserSerializer
    
    def post(self, request):
        data = json.loads(request.body)
        data['first_name'] = data.pop('name')
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if user is None:
                return Response(status=409)
            login(user=user, request=request)
            if request.session.get('orderId'):
                order = Order.objects.get(id=request.session['orderId'])
                order.customer = user
                order.save() 
            return Response(status=200)
        return Response(status=409)