from django.db import models
from django.contrib.auth.models import User
from product_api.models import Product


class Order(models.Model):
    delivery_choices = (
        ('express', 'Express'),
        ('ordinary', 'Ordinary'),
    )
    payment_choices = (
        ('online', 'Online'),
        ('someone', 'Someone'),
    )
    status_choices = (
    ('accepted', 'Accepted'),
    ('processing', 'Processing'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ('created', 'Created')
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    deliveryType = models.CharField(choices=delivery_choices, max_length=50)
    paymentType = models.CharField(choices=payment_choices, max_length=50)
    totalCost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=status_choices, max_length=50)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)
    

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products_in_order')
    
    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'
        
    def __str__(self):
        return str(self.id)