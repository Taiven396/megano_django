import random
from .models import Product, Review, Tags, Category
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from .pagination import SalePagination, CatalogFilterPagination
from .serializers import (
    TagsSerializers,
    ProductSerializer,
    CatalogSerializer,
    SaleSerializer,
)


class TagsListApiView(ListAPIView):
    model = Tags
    serializer_class = TagsSerializers
    queryset = Tags.objects.all()


class CategoryListApiView(ListAPIView):
    serializer_class = CatalogSerializer
    queryset = Category.objects.prefetch_related("subcategories").all()


class PopularProductListApiView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Возвращает набор случайно выбранных популярных товаров.
        Получает набор всех популярных товаров,
        включая предварительную загрузку связанных
        моделей 'image', 'tags' и 'reviews'.
        Затем случайным образом выбирает 4 товара из набора.
        Возвращается набор случайно выбранных популярных товаров.
        """
        queryset = Product.objects.prefetch_related("image", "tags", "reviews").filter(
            popular=True
        )
        queryset = random.sample(list(queryset), 4)
        return queryset


class LimitedProductListApiView(ListAPIView):
    """
    Api представление, возвращает список
    лимитированных товаров. Подгружает картинки,
    тэги и отзывы
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Возвращает набор случайно выбранных лимитированных товаров.
        Получает набор всех лимитированных товаров,
        включая предварительную загрузку связанных
        моделей 'image', 'tags' и 'reviews'.
        Затем случайным образом выбирает 4 товара из набора.
        Возвращается набор случайно выбранных лимитированных товаров.
        """
        queryset = Product.objects.prefetch_related("image", "tags", "reviews").filter(
            limited=True
        )
        queryset = random.sample(list(queryset), 4)
        return queryset


class BannersListApiView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Возвращает набор случайно выбранных лимитированных товаров,
        для баннеров. Получает набор всех лимитированных товаров,
        включая предварительную загрузку связанных
        моделей 'image', 'tags' и 'reviews'.
        Затем случайным образом выбирает 4 товара из набора.
        Возвращается набор случайно выбранных лимитированных товаров.
        """
        queryset = Product.objects.prefetch_related("image", "tags", "reviews").filter(
            limited=True
        )
        queryset = random.sample(list(queryset), 2)
        return queryset


class SaleListApiView(ListAPIView):
    serializer_class = SaleSerializer
    queryset = (
        Product.objects.prefetch_related("image").order_by("id").filter(sale=True)
    )
    pagination_class = SalePagination


class CatalogCategory(ListAPIView):
    model = Category


class CatalogFilterListApiView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CatalogFilterPagination

    def get_queryset(self):
        """
        Получает параметры фильтрации и сортировки из параметров запроса.
        Использует параметры для фильтрации и сортировки набора товаров.
        Возвращается отфильтрованный и отсортированный набор товаров.
        """
        min_price = int(self.request.GET.get("filter[minPrice]"))
        max_price = int(self.request.GET.get("filter[maxPrice]"))
        sort = self.request.GET.get("sort")
        sort_type = self.request.GET.get("sortType")
        available = self.request.GET.get("filter[available]")
        name = self.request.GET.get("filter[name]")
        tags = self.request.GET.getlist("tags[]")
        free_delivery = self.request.GET.get("filter[freeDelivery]")
        queryset = Product.objects.prefetch_related("image", "tags").all()
        queryset = queryset.filter(Q(price__lte=max_price) & Q(price__gte=min_price))
        if available == "true":
            queryset = queryset.filter(count__gt=0)
        else:
            queryset = queryset.filter(count__lte=0)
        if len(tags) > 0:
            queryset = queryset.filter(tags__in=tags)
        if sort_type == "dec":
            queryset = queryset.order_by(sort)
        elif sort_type == "inc":
            queryset = queryset.order_by("-" + sort)
        if free_delivery == "true":
            queryset = queryset.filter(freeDelivery=True)
        if len(name) > 0:
            queryset = queryset.filter(title__icontains=name)
        unique = []
        for product in queryset:
            if product not in unique:
                unique.append(product)
        return unique


class ProductListApiView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = (
        Product.objects.select_related("category")
        .prefetch_related("tags", "image", "reviews", "specifications")
        .all()
    )

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос и создает
        новый отзыв для товара. Получает идентификатор
        товара из параметров запроса (kwargs['pk']).
        Проверяет наличие пользователя по указанному
        автору (request.data['author']), и если пользователь
        не существует, возвращает статус 409 (Conflict).
        Затем проверяет соответствие пользователя, отправившего
        запрос, с указанным автором и адресом электронной почты,
        и если они не совпадают, также возвращает статус 409.
        Создает новый объект отзыва с указанными данными и сохраняет его.
        Возвращает объект Response со статусом 200 в случае успешного создания отзыва.
        """
        product = Product.objects.get(id=kwargs["pk"])
        try:
            user = User.objects.get(username=request.data["author"])
        except User.DoesNotExist:
            return Response(status=409)
        if (
            user.username != request.user.username
            or user.profile.email != request.data["email"]
        ):
            return Response(status=409)
        Review.objects.create(
            author=user,
            text=request.data["text"],
            rate=request.data["rate"],
            product=product,
            checked=False,
        )
        return Response(status=200)
