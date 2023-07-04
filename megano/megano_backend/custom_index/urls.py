from  django.urls import  path
from django.views.generic import TemplateView

from .views import product_form_view, ProductAutocompleteView


app_name = 'history_order'

urlpatterns = [
    path('custom-index/', product_form_view, name='custom-index'),
    path('product-autocomplete/', ProductAutocompleteView.as_view(), name='product-autocomplete'),
    path('product/<int:id>/', TemplateView.as_view(template_name='history_order/product.html'), name='custom-product')
]