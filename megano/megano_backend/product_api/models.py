from django.db import models
from catalog_api.models import Category, Subcategory
from tags_api.models import Tags
from django.contrib.auth.models import User

def upload_path_images(instanse, filename):
    return f'products_images/product{instanse.id}/{filename}'


class Specifications(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=300)
    
    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'
        
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tags, blank=True)    
    popular = models.BooleanField(default=False)
    sale = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    fullDescription = models.TextField()
    salePrice = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    freeDelivery = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    count = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    specifications = models.ForeignKey(Specifications, on_delete=models.PROTECT, null=True, blank=True, related_name='specifications')
    dateFrom = models.CharField(max_length=12, blank=True, null=True)
    dateTo = models.CharField(max_length=12, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        
    def __str__(self):
        return self.title
    
    
class ProductImages(models.Model):
    image = models.ImageField(upload_to=upload_path_images)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    
    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктоа'
    
    def __str__(self):
        return str(self.id)    
        
class Review(models.Model):
    rate_list = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.PositiveIntegerField(choices=rate_list)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name='reviews')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        
    def __str__(self):
        return str(self.rate)