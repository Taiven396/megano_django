from django.contrib import admin
from .models import Order, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "address", "customer", "status"]
    list_filter = ["status"]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "count"]
