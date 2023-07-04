from django.contrib import admin
from .models import Product, Specifications, Review, ProductImages



@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'checked']
    list_filter = ['checked']

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'sale', 'popular', 'limited', 'date']
    autocomplete_fields = ['category', 'subcategory', 'tags', 'specifications']