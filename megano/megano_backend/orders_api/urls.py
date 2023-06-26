from django.urls import path
from .views import OrderRetrieveUpdateApiView


app_name = 'orders_api'

urlpatterns = [
    path('orders', OrderRetrieveUpdateApiView.as_view(), name='orders')
]