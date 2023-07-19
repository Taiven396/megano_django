from typing import Dict
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from .models import Order, OrderProduct
from product_api.models import Product
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from config_data import config
import smtplib
from .serializers import (
    OrderSerializer,
    BasketSerializer,
    PaymentSerializer,
)


class BasketApiView(ListAPIView):
    serializer_class = BasketSerializer

    def data(self):
        """
        Сериализует данные набора товаров из корзины.
        Получает набор данных товаров из функции
        get_queryset() и выполняет их сериализацию
        с использованием сериализатора BasketSerializer.
        Контекст сериализатора передается из сессии ('cart').
        Возвращает сериализованные данные товаров.
        """
        queryset = self.get_queryset()
        serializer = BasketSerializer(
            queryset, context=self.request.session["cart"], many=True
        )
        return serializer.data

    def get_queryset(self):
        """
        Возвращает набор данных товаров,
        отфильтрованных на основе идентификаторов,
        хранящихся в корзине. Получает список товаров
        из сессии ('cart') и извлекает их идентификаторы.
        Затем выполняет запрос к модели Product с
        выборкой связанных моделей 'category' и 'image'.
        Возвращается набор товаров, чьи идентификаторы
        присутствуют в списке.
        """
        products = self.request.session["cart"]
        ids = list()
        for i in products:
            ids.append(i["id"])
        data = (
            Product.objects.select_related("category")
            .prefetch_related("image")
            .filter(id__in=ids)
        )
        return data

    def delete(self, request: Request) -> Response:
        """
        Получает идентификатор товара (product_id)
        и количество (count) из данных запроса.
        Проверяет наличие товара в корзине и уменьшает
        его количество на указанное значение.
        Если количество достигает 0, удаляет товар из корзины.
        Возвращает объект Response с данными о корзине
        """
        product_id = request.data["id"]
        count = int(request.data["count"])
        for index, value in enumerate(request.session["cart"]):
            if next(iter(value.values())) == product_id:
                request.session["cart"][index]["count"] -= count
                if request.session["cart"][index]["count"] == 0:
                    request.session["cart"].remove(request.session["cart"][index])
                request.session.save()
        return Response(self.data())

    def get(self, request: Request) -> Response:
        """
        Возвращает объект Response с данными о корзине.
        """
        return Response(self.data())

    def post(self, request: Request) -> Response:
        """
        Получает идентификатор товара (product_id)
        и количество (count) из данных запроса.
        Если 'cart' уже существует в сессии,
        проверяет наличие товара в корзине.
        Если товар уже присутствует, увеличивает
        его количество на указанное значение.
        Если товар отсутствует, добавляет его
        в корзину с указанным количеством.
        Если 'cart' отсутствует в сессии, создает новую
        корзину и добавляет товар с указанным количеством.
        Возвращает объект Response с данными о корзине.
        """
        product_id = request.data["id"]
        count = int(request.data["count"])
        if "cart" in request.session:
            for index, value in enumerate(request.session["cart"]):
                if next(iter(value.values())) == product_id:
                    request.session["cart"][index]["count"] += count
                    request.session.save()
                    return Response(self.data())
            request.session["cart"].append({"id": product_id, "count": count})
            request.session.save()
            return Response(self.data())
        request.session["cart"] = [{"id": product_id, "count": count}]
        request.session.save()
        return Response(self.data())


class OrderListApiView(ListAPIView):
    model = Order
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Возвращает набор данных заказов,
        отфильтрованных по определенным критериям.
        Запрос включает предварительную загрузку
        связанных моделей 'products_in_order'.
        Возвращается только заказы, принадлежащие
        текущему пользователю (self.request.user)
        и имеющие статус 'created'.
        """
        queryset = Order.objects.prefetch_related("products_in_order").filter(
            customer=self.request.user, status="created"
        )
        return queryset

    def post(self, request: Request) -> Response:
        """
        Для каждого товара в запросе вычисляется
        стоимость, создается связь между заказом и товаром,
        общая стоимость заказа сохраняется, сессия 'cart'
        очищается, а идентификатор заказа сохраняется в сессии.
        Возвращает объект Response со статусом 200 и данными,
        включающими идентификатор созданного заказа.
        """
        total_cost = 0
        order = Order.objects.create(
            totalCost=0,
            status="created",
            customer=request.user if request.user.username else None,
        )
        for i_product in request.data:
            cost = float(i_product["price"]) * int(i_product["count"])
            total_cost += cost
            product = Product.objects.get(id=i_product["id"])
            OrderProduct.objects.create(
                order=order,
                product=product,
                count=i_product["count"],
            )
            order.totalCost = total_cost
            order.status = "Cоздан"
            order.save()
            request.session["cart"] = []
            data = {"orderId": order.id}
            request.session["orderId"] = order.id
            return Response(status=200, data=data)


class OrderRetrieveApiView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related("products_in_order").all()

    def get(self, request: Request, *args, **kwargs: Dict):
        """
        Если пользователь является владельцем заказа,
        вызывается базовая реализация метода get.
        Если пользователь не является владельцем заказа,
        вызывается исключение PermissionDenied.
        """
        self.object = self.get_object()
        if request.user == self.object.customer:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def post(self, request: Request, *args, **kwargs: Dict) -> Response:
        """
        Получает идентификатор заказа из запроса и
        обновляет соответствующие атрибуты заказа,
        такие как город, адрес, тип оплаты и тип доставки.
        Возвращает объект Response со статусом 200 и данными,
        включающими идентификатор заказа.
        """
        order = Order.objects.get(id=request.data["orderId"])
        order.city = request.data["city"]
        order.address = request.data["address"]
        if request.data["paymentType"] == "cash":
            order.paymentType = "Оплата наличными"
            mail_send(
                mail=order.customer.profile.email,
                order=order.id,
                name=order.customer.profile.fullName,
            )
        else:
            order.paymentType = "Онлайн оплата"
        order.deliveryType = request.data["deliveryType"]
        order.status = "подтвержден"
        order.save()
        return Response(
            {"orderId": order.id, "paymentType": order.paymentType}, status=200
        )


class ProgressPayment(APIView):
    def get(self, request, *args, **kwargs):
        return Response(status=200)


class PaymentRetrieveApiView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Order.objects.prefetch_related("products_in_order").all()

    def post(self, request: Request, *args, **kwargs: Dict) -> Response:
        """
        Получает данные из запроса и создает экземпляр
         PaymentSerializer для их валидации.
        Затем получает объект заказа по его
        идентификатору (kwargs['pk']).
        Если данные платежа являются валидными,
        отправляется электронное письмо и статус заказа
        обновляется на 'accepted'.
        Возвращает объект Response со статусом 200 в случае
        успешной обработки или 500 в случае ошибки.
        """
        data = request.data
        serializer = PaymentSerializer(data=data)
        order = Order.objects.get(id=kwargs["pk"])
        if serializer.is_valid():
            mail_send_paid(
                mail=order.customer.profile.email,
                order=kwargs["pk"],
                name=order.customer.profile.fullName,
            )
            order.status = "оплачен"
            order.save()
            url = "custom_index:progress"
            return Response(status=200)
        return Response(status=500)


def mail_send(mail: str, order: str, name: str) -> None:
    """
    Отправляет электронное письмо с
    информацией о подтверждении заказа.
    Получает адрес электронной почты получателя (mail),
    номер заказа (order) и имя получателя (name).
    Отправитель, тема письма и текст письма
    формируются на основе полученных данных.
    Используется SMTP-сервер yandex.com для отправки письма.
    """
    email = "Megano-Shop@yandex.ru"
    password = config.MAIL_PASSWORD
    subject = f"Заказ {order}"
    email_text = (
        f"Уважаемый(ая) {name},\n\n"
        f"Мы рады сообщить вам, что ваш заказ номер {order} подтвержден.\n"
        f"Спасибо за доверие и выбор нашей компании!\n\n"
        f"Мы уже начали обработку вашего заказа и скоро доставим его по указанному адресу.\n"
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


def mail_send_paid(mail: str, order: str, name: str) -> None:
    """
    Отправляет электронное письмо с
    информацией о подтверждении заказа.
    Получает адрес электронной почты получателя (mail),
    номер заказа (order) и имя получателя (name).
    Отправитель, тема письма и текст письма
    формируются на основе полученных данных.
    Используется SMTP-сервер yandex.com для отправки письма.
    """
    email = "Megano-Shop@yandex.ru"
    password = config.MAIL_PASSWORD
    subject = f"Заказ {order}"
    email_text = (
        f"Уважаемый(ая) {name},\n\n"
        f"Мы рады сообщить вам, что ваш заказ номер {order} успешно оплачен.\n"
        f"Спасибо за доверие и выбор нашей компании!\n\n"
        f"Мы уже начали обработку вашего заказа и скоро доставим его по указанному адресу.\n"
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
