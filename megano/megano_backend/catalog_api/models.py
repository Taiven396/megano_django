from django.db import models


def category_photo_path(instanse, filename):
    return f'category/{instanse.title}/{filename}'


def subcategory_photo_path(instanse, filename):
    return f'subcategory/{instanse.title}/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=200)
    images = models.ImageField(upload_to=category_photo_path)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        

class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=subcategory_photo_path)
    parent = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='subcategories')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'