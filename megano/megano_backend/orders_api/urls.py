from django.urls import path
from .views import OrderListApiView, OrderRetrieveApiView, PaymentRetrieveApiView


app_name = 'orders_api'

urlpatterns = [
    path('orders', OrderListApiView.as_view(), name='orders'),
    path('orders/<int:pk>', OrderRetrieveApiView.as_view(), name='order'),
    path('order/<int:pk>', OrderRetrieveApiView.as_view(), name='order-pk'),
    path('payment/<int:pk>', PaymentRetrieveApiView.as_view(), name='payment')
]