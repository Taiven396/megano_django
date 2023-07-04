from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Category
from product_api.models import Product
from .pagination import SalePagination, CatalogFilterPagination
from django.db.models import Q
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
    """
    Api представление, возвращает список
    популярных товаров. Подгружает картинки,
    тэги и отзывы
    """
    serializer_class = PopularProductSerializer
    queryset = Product.objects.prefetch_related('image', 'tags', 'reviews').filter(popular=True)
    

class LimitedProductListApiView(ListAPIView):
    """
    Api представление, возвращает список
    лимитированных товаров. Подгружает картинки,
    тэги и отзывы
    """
    serializer_class = LimitedProductSerializer
    queryset = Product.objects.prefetch_related('image', 'tags', 'reviews').filter(limited=True)
    
    
class BannersListApiView(ListAPIView):
    """
    Api представление, возвращает список
    товаров для баннеров. Подгружает картинки,
    тэги и отзывы
    """
    serializer_class = BannersSerializer
    queryset = Product.objects.prefetch_related(
        'image', 'tags', 'reviews').filter(limited=True)
    
    
class SaleListApiView(ListAPIView):
    """
    Api представление, возвращает список
    товаров на распродаже. Подгружает картинки.
    """
    serializer_class = SaleSerializer
    queryset = Product.objects.prefetch_related(
        'image').order_by('id').filter(sale=True)
    pagination_class = SalePagination


class CatalogFilterListApiView(ListAPIView):
    """
    Api представление, возвращает список
    товаров по фильтрам. Подгружает картинки.
    """
    serializer_class = PopularProductSerializer
    pagination_class = CatalogFilterPagination

    def get_queryset(self):
        min_price = int(self.request.GET.get('filter[minPrice]'))
        max_price = int(self.request.GET.get('filter[maxPrice]'))
        sort = self.request.GET.get('sort')
        sort_type = self.request.GET.get('sortType')
        available = self.request.GET.get('filter[available]')
        name = self.request.GET.get('filter[name]')
        tags = self.request.GET.getlist('tags[]')
        free_delivery = self.request.GET.get('filter[freeDelivery]')
        queryset = Product.objects.prefetch_related('image', 'tags').all()
        queryset = queryset.filter(Q(price__lte=max_price) & Q(price__gte=min_price))
        if available == 'true':
            queryset = queryset.filter(count__gt=0)
        else:
            queryset = queryset.filter(count__lte=0)
        if len(tags) > 0:
            queryset = queryset.filter(tags__in=tags)
        if sort_type == 'dec':
            queryset = queryset.order_by(sort)
        elif sort_type == 'inc':
            queryset = queryset.order_by('-'+sort)
        if free_delivery == 'true':
            queryset = queryset.filter(freeDelivery=True)
        if len(name) > 0:
            queryset = queryset.filter(title__contains=name)
        queryset = queryset.distinct()                          
        return queryset