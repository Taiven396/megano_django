from django_select2.forms import ModelSelect2Widget
from django import forms
from product_api.models import Product


class ProductForm(forms.Form):
    title = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=ModelSelect2Widget(
            data_view="custom_index:product-autocomplete",
            attrs={"class": "form-control w-100"},
        ),
    )
