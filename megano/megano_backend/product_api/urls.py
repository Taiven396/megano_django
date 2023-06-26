from django.urls import path
from .views import (
    ProductRetrievApiView,
)

app_name = 'product_api'

urlpatterns = [
    path('product/<int:pk>', ProductRetrievApiView.as_view(), name='product-api'),
]