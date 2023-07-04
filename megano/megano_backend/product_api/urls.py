from django.urls import path
from .views import (
    ProductListApiView,
)

app_name = 'product_api'

urlpatterns = [
    path('product/<int:pk>', ProductListApiView.as_view(), name='product-api'),
    path('product/<int:pk>/reviews', ProductListApiView.as_view(), name='product-review')
]