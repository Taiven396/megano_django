from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Category
from product_api.models import Product
from .pagination import SalePagination
from .serializers import (
    CatalogSerializer,
    PopularProductSerializer,
    LimitedProductSerializer,
    BannersSerializer,
    SaleSerializer,
)


class CategoryListApiView(ListAPIView):
    """
    Возвращает список всех категорий товаров,
    подгружает связанные подкатегории.
    """
    serializer_class = CatalogSerializer
    queryset = Category.objects.prefetch_related('subcategories').all()


class PopularProductListApiView(ListAPIView):
    serializer_class = PopularProductSerializer
    queryset = Product.objects.prefetch_related('image', 'tags', 'reviews').filter(popular=True)
    

class LimitedProductListApiView(ListAPIView):
    serializer_class = LimitedProductSerializer
    queryset = Product.objects.prefetch_related('image', 'tags', 'reviews').filter(limited=True)
    
    
class BannersListApiView(ListAPIView):
    serializer_class = BannersSerializer
    queryset = Product.objects.prefetch_related('image', 'tags', 'reviews').filter(limited=True)
    
    
class SaleListApiView(ListAPIView):
    serializer_class = SaleSerializer
    queryset = Product.objects.prefetch_related('image').order_by('id').filter(sale=True)
    pagination_class = SalePagination

