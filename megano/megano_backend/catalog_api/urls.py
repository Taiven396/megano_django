from django.urls import path
from .views import (
    CategoryListApiView,
    PopularProductListApiView,
    LimitedProductListApiView,
    BannersListApiView,
    SaleListApiView,
)


app_name = 'catalog_api'

urlpatterns = [
    path('categories', CategoryListApiView.as_view(), name='categories'),
    path('products/popular', PopularProductListApiView.as_view(), name='popular-products'),
    path('products/limited', LimitedProductListApiView.as_view(), name='limited-products'),
    path('banners/', BannersListApiView.as_view(), name='banners'),
    path('sales/', SaleListApiView.as_view(), name='sales')
]