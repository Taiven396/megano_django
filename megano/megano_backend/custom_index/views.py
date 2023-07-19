from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .serializers import OrderSerializer
from .forms import ProductForm
from orders_api.models import Order
from product_api.models import Product
from django.contrib.syndication.views import Feed


class VerificationCode(TemplateView):
    template_name = "custom_index/code.html"

    def post(self, request, *args, **kwargs):
        data = request.POST
        code = request.session["code"]
        if data["code"] != code:
            messages.error(request, "Введен неверный код")
            return redirect("custom_index:code")
        user = User.objects.get(id=request.session["user_id"])
        user.is_active = True
        user.save()
        login(user=user, request=request)
        return redirect("custom_index:custom-index")


class SaleProductFeed(Feed):
    title = "Megano-Shop sale"
    link = "/product/"
    description = "Products on sale"

    def items(self):
        return Product.objects.filter(sale=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        image = item.image.all()
        return (
            f"<p>{item.description}</p>"
            f"<p> Старая цена: {item.price}$, Цена по скидке: {item.salePrice}$</p>"
            f'<img src="{image[0].image.url}">'
            f"<p> Только до {item.dateTo}</p>"
        )

    def item_link(self, item):
        return "/product/" + str(item.id)


class CustomIndex(TemplateView):
    form = ProductForm
    template_name = "custom_index/custom-index.html"

    def post(self, request, *args, **kwargs):
        return redirect(
            reverse_lazy(
                "custom_index:custom-product", kwargs={"id": request.POST.get("title")}
            )
        )

    def get(self, *args, **kwargs):
        return render(
            self.request, "custom_index/custom-index.html", {"product_form": self.form}
        )


class ProductAutocompleteView(View):
    def get(self, request):
        q = request.GET.get("q", "")
        products = Product.objects.filter(title__contains=q)
        results = [{"id": product.id, "text": product.title} for product in products]
        return JsonResponse({"results": results})


class OrderListView(TemplateView):
    template_name = "custom_index/historyorder.html"

    def get_queryset(self):
        queryset = (
            Order.objects.prefetch_related("products_in_order")
            .filter(customer=self.request.user)
            .exclude(status="создан")
        )
        return queryset

    def get(self, request, *args, **kwargs):
        data = OrderSerializer(data=self.get_queryset(), many=True)
        data.is_valid()
        data = data.data
        return render(
            request,
            template_name="custom_index/historyorder.html",
            context={"orders": data},
        )
