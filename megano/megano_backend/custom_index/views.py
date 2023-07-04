from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from .forms import ProductForm
from product_api.models import Product


def product_form_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        print(request.POST)
        return redirect(reverse_lazy('history_order:custom-product', kwargs={'id': request.POST.get('title')}))
    else:
        form = ProductForm()
    return render(request, 'history_order/custom-index.html', {'product_form': form})


class ProductAutocompleteView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        products = Product.objects.filter(title__contains=q)
        results = [{'id': product.id, 'text': product.title} for product in products]
        return JsonResponse({'results': results})