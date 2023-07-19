from config_data import config
import smtplib
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from orders_api.models import Order
import datetime
import logging
import json
import random

from .models import Profile
from .serializers import (
    UserSerializer,
    LogInSerializer,
    ProfileSerializer,
    ProfileAvatarSerializer,
    PasswordSerializer,
)


logger_info = logging.getLogger("info_log")


class ProfileRetrievUpdateView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        """
        Возвращает Profile пользователя
        """
        return self.request.user.profile

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Получает данные из запроса (request.data) и если данные
        валидны, обновляет профиль пользователя с помощью
        сохранения в соответствующих полях.
        Получает сериализованные данные обновленного профиля и
        возвращает объект Response с данными и статусом 200.
        Если данные невалидны, возвращает объект Response с
        сообщением об ошибке и статусом 409.
        """
        data = request.data
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            profile = request.user.profile
            profile.fullName = request.data["fullName"]
            profile.phone = request.data["phone"]
            profile.email = request.data["email"]
            profile.save()
            data = self.get_serializer(self.request.user.profile).data
            return Response(status=200, data=data)
        data = {"error": "Невалидные данные"}
        return Response(status=409, data=data)


class ProfileAvatarUpdateView(RetrieveAPIView):
    serializer_class = ProfileAvatarSerializer

    def get_object(self):
        """
        Возвращает Profile пользователя
        """
        return self.request.user.profile

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Обрабатывает POST-запрос и обновляет
        аватар пользователя. Проверяет наличие аватара
        в данных запроса (request.data['avatar']).
        Если аватар присутствует, обновляет аватар пользователя
        с помощью сохранения в поле 'avatar' профиля пользователя.
        Возвращает объект Response со статусом 200 в
        случае успешного обновления.
        """
        if request.data["avatar"]:
            profile = request.user.profile
            profile.avatar = request.FILES["avatar"]
            profile.save()
        return Response(status=200)


class PasswordApiView(APIView):
    def post(self, request: Request) -> Response:
        """
        Изменяет пароль пользователя, внутри
        сериализатора
        """
        data = request.data
        data["username"] = request.user.username
        print(data)
        serializer = PasswordSerializer(data=data)
        if serializer.is_valid():
            return Response(status=200)
        return Response(status=400)


class SignInApiView(APIView):
    def post(self, request: Request) -> Response:
        """
        Извлекает пользователя из базы данных на
        основе полученного имени пользователя (data['username']).
        Создает экземпляр сериализатора LogInSerializer
        с полученными данными. Если данные валидны, выполняет
        авторизацию пользователя с помощью функции login.
        Если в сессии есть 'orderId', привязывает
        пользователя к соответствующему заказу.
        Возвращает статус 200 в случае успешного входа.
        Если данные неверны или происходит ошибка, возвращает
        статус 409 с сообщением об ошибке.
        """
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data["username"])
            if not user.is_active:
                return Response(status=409)
            serialize = LogInSerializer(data=data)
            if serialize.is_valid():
                login(user=user, request=request)
                if request.session.get("orderId"):
                    order = Order.objects.get(id=request.session["orderId"])
                    order.customer = user
                    order.save()
                return Response(status=200)
        except:
            return Response(status=409)


class SignOutApi(APIView):
    def post(self, request: Request) -> Response:
        """
        Выполняет выход пользователя из системы
        с помощью функции logout. Возвращает объект
        Response со статусом 200 в случае успешного выхода.
        """
        logger_info.info(
            f"Пользователь {request.user.username} успешно "
            f"вышел из системы. {datetime.datetime.now()}"
        )
        logout(request=request)
        return Response(status=200)


class SignUpCreateApiView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request) -> Response:
        """
        Обрабатывает POST-запрос и создает нового
        пользователя на основе полученных данных.
        Создает экземпляр сериализатора с полученными данными.
        Если данные валидны, сохраняет пользователя
        и выполняет его авторизацию. Если пользователь не может
        быть сохранен, возвращает статус 409 (Conflict).
        Если в сессии есть 'orderId', привязывает пользователя
        к соответствующему заказу. Возвращает статус 200 в
        случае успешного создания пользователя и авторизации.
        """
        data = json.loads(request.body)
        data["first_name"] = data.pop("name")
        print(data)
        try:
            Profile.objects.get(email=data["email"])
            return Response(status=409)
        except Exception:
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                if user is None:
                    return Response(status=409)
                if request.session.get("orderId"):
                    order = Order.objects.get(id=request.session["orderId"])
                    order.customer = user
                    order.save()
                code = str(random.randint(100000, 999999))
                request.session["code"] = code
                request.session["user_id"] = user.id
                mail_send_code(mail=data["email"], code=code, name=data["first_name"])
                return Response(status=200)
            return Response(status=409)


def mail_send_code(mail: str, code: str, name: str) -> None:
    """
    Отправляет электронное письмо с
    проверочным кодом. Получает адрес
    электронной почты получателя (mail),
    код (code). Отправитель, тема письма
    и текст письма формируются на основе полученных данных.
    Используется SMTP-сервер yandex.com для отправки письма.
    """
    email = "Megano-Shop@yandex.ru"
    password = config.MAIL_PASSWORD
    subject = f"Проверочный код"
    email_text = (
        f"Уважаемый(ая) {name},\n\n"
        f"Ваш проверочный код: {code}.\n"
        f"С наилучшими пожеланиями,\n"
        f"Команда Megano"
    )
    message = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(
        email, mail, subject, email_text
    ).encode("utf-8")
    server = smtplib.SMTP_SSL("smtp.yandex.com")
    server.set_debuglevel(1)
    server.login(email, password)
    server.sendmail(email, mail, message)
    server.quit()
    return
