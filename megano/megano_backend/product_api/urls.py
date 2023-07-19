from django.urls import path
from .views import (
    ProductListApiView,
    TagsListApiView,
    CategoryListApiView,
    PopularProductListApiView,
    LimitedProductListApiView,
    BannersListApiView,
    SaleListApiView,
    CatalogFilterListApiView,
    CatalogCategory,
)

app_name = "product_api"

urlpatterns = [
    path("product/<int:pk>", ProductListApiView.as_view(), name="product-api"),
    path(
        "product/<int:pk>/reviews", ProductListApiView.as_view(), name="product-review"
    ),
    path("tags", TagsListApiView.as_view(), name="tags-api"),
    path("categories", CategoryListApiView.as_view(), name="categories"),
    path(
        "products/popular", PopularProductListApiView.as_view(), name="popular-products"
    ),
    path(
        "products/limited", LimitedProductListApiView.as_view(), name="limited-products"
    ),
    path("banners", BannersListApiView.as_view(), name="banners"),
    path("sales", SaleListApiView.as_view(), name="sales"),
    path("catalog", CatalogFilterListApiView.as_view(), name="catalog"),
    path("catalog/<int:pk>", CatalogFilterListApiView.as_view(), name="catalog"),
]
