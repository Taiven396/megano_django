from django.urls import path
from django.views.generic import TemplateView

from .views import OrderListApiView, OrderRetrieveApiView, PaymentRetrieveApiView, BasketApiView


app_name = 'frontend'

urlpatterns = [
    path('orders', OrderListApiView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderRetrieveApiView.as_view(), name='order'),
    path('order/<int:pk>', OrderRetrieveApiView.as_view(), name='order-pk'),
    path('payment/<int:pk>', PaymentRetrieveApiView.as_view(), name='payment'),
    path('basket', BasketApiView.as_view(), name='basket'),
]