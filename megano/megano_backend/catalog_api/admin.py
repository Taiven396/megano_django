from django.contrib import admin
from .models import Category, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']
    
    
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    search_fields = ['title']
    
    