from  django.urls import  path
from django.views.generic import TemplateView

from .views import ProductAutocompleteView, CustomIndex, SaleProductFeed, OrderListView


app_name = 'custom_index'

urlpatterns = [
    path('custom/', CustomIndex.as_view(), name='custom-index'),
    path('product-autocomplete/', ProductAutocompleteView.as_view(), name='product-autocomplete'),
    path('product/<int:id>/', TemplateView.as_view(template_name='custom_index/product.html'), name='custom-product'),
    path('feed/', SaleProductFeed(), name='feed'),
    path('historyorder/', OrderListView.as_view())
    ]
