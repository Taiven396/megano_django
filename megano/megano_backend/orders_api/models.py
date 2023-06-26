from django.db import models
from django.contrib.auth.models import User
from product_api.models import Product


class Order(models.Model):
    delivery_choices = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
    payment_choices = (
        ('online', 'Online'),
        ('cash', 'Cash'),
    )
    status_choices = (
    ('accepted', 'Accepted'),
    ('processing', 'Processing'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed')
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveryType = models.CharField(choices=delivery_choices, max_length=50)
    paymentType = models.CharField(choices=payment_choices, max_length=50)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=status_choices, max_length=50)
    city = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        
    def __str__(self):
        return self.address
    

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'
        
    def __str__(self):
        return str(self.id)