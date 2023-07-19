from django.db import models
from django.contrib.auth.models import User


def category_photo_path(instanse, filename):
    return f"category/{instanse.title}/{filename}"


def subcategory_photo_path(instanse, filename):
    return f"subcategory/{instanse.title}/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=200)
    images = models.ImageField(upload_to=category_photo_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=subcategory_photo_path)
    parent = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="subcategories"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


def upload_path_images(instanse, filename):
    return f"products_images/product{instanse.product.id}/{filename}"


class Tags(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Specifications(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=300)
    product = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Спецификация"
        verbose_name_plural = "Спецификации"

    def __str__(self):
        return self.product + " " + self.name


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
    specifications = models.ManyToManyField(
        Specifications, blank=True, related_name="specifications"
    )
    dateFrom = models.CharField(max_length=12, blank=True, null=True)
    dateTo = models.CharField(max_length=12, blank=True, null=True)
    rating = models.FloatField(default=0)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def update_rating(self):
        rate_points = [review.rate for review in Review.objects.filter(product=self)]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            self.rating = rating
        else:
            self.rating = 0

    def save(self, *args, **kwargs):
        self.update_rating()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    image = models.ImageField(upload_to=upload_path_images)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    rate_list = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.PositiveIntegerField(choices=rate_list)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, null=True, blank=True, related_name="reviews"
    )
    checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return str(self.rate)
