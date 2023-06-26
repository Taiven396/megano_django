from django.urls import path
from .views import BasketApiView

app_name = 'basket_api'

urlpatterns = [
    path('basket', BasketApiView.as_view(), name='basket')
]