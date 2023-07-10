from django.contrib import admin
from .models import (
    Product,
    Specifications,
    Review,
    ProductImages,
    Tags,
    Category,
    Subcategory
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'checked']
    list_filter = ['checked']

@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'product']
    search_fields = ['product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'sale', 'popular', 'limited', 'date']
    autocomplete_fields = ['category', 'subcategory', 'tags', 'specifications']
    search_fields = ['title']

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']