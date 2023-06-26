from django.contrib import admin
from .models import Product, Specifications, Review, ProductImages



@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'sale', 'popular', 'limited', 'date']