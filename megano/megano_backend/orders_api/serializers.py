from  rest_framework import serializers
from .models import Order
from product_api.models import Product, Review


class BasketSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price',
            'count', 'date', 'title',
            'description', 'freeDelivery', 'images',
            'tags', 'reviews', 'rating']

    def get_count(self, obj):
        data = self.context
        for i in data:
            count = i['count']
            if next(iter(i.values())) == obj.id:
                return count

    def get_price(self, obj):
        if obj.sale:
            return obj.salePrice
        return obj.price

    def get_images(self, obj):
        return [{
            'src': image.image.url,
            'alt': image.image.name
        }
            for image in obj.image.all()
        ]

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        rate_points = [review.rate for review in Review.objects.filter(product=obj).all()]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            return rating
        return 0

    def get_tags(self, obj):
        tags = [tag.name for tag in obj.tags.all()]
        print(tags)
        return [
            tag.name
            for tag in obj.tags.all()
        ]

class ProductInOrderSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'price',
                  'count', 'date', 'title', 'description',
                  'freeDelivery', 'images',
                  'tags', 'reviews', 'rating']

    def get_price(self, obj):
        if obj.product.sale:
            return obj.product.salePrice
        return obj.product.price

    def get_description(self, obj):
        return obj.product.description

    def get_id(self, obj):
        return obj.product.id

    def get_title(self, obj):
        return obj.product.title

    def get_price(self, obj):
        if obj.product.sale:
            return obj.product.salePrice
        return obj.product.price

    def get_category(self, obj):
        return obj.product.category.id

    def get_images(self, obj):
        return [{
            'src': image.image.url,
            'alt': image.image.name
        }
            for image in obj.product.image.all()
        ]

    def get_tags(self, obj):
        tags = [tag.name for tag in obj.product.tags.all()]
        print(tags)
        return [
            tag.name
            for tag in obj.product.tags.all()
        ]

    def get_reviews(self, obj):
        return [
            {
                'author': review.author.username,
                'email': review.author.profile.email,
                'text': review.text,
                'rate': review.rate,
                'date': review.date
            }
            for review in obj.product.reviews.all()
        ]

    def get_rating(self, obj):
        rate_points = [review.rate for review in Review.objects.filter(product=obj.product).all()]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            return rating
        return 0


class OrderSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField(source='products_in_order')
    createdAt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'createdAt','fullName', 'email', 'deliveryType',
            'paymentType', 'phone', 'totalCost',
            'status', 'city', 'address', 'products'
        ]

    def get_createdAt(self, obj):
        return obj.createdAt.strftime('%Y-%m-%d %H:%M')

    def get_fullName(self, obj):
        return obj.customer.profile.fullName

    def get_email(self, obj):
        return obj.customer.profile.email

    def get_phone(self, obj):
        return obj.customer.profile.phone

    def get_products(self, obj):
        products_in_order = obj.products_in_order.all()
        products = [ product for product in products_in_order ]
        serializer = ProductInOrderSerializer(data=products, many=True)
        serializer.is_valid()
        return serializer.data


class PaymentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    number = serializers.CharField(max_length=16, min_length=16)
    code = serializers.CharField(max_length=3, min_length=3)
    month = serializers.CharField(min_length=2, max_length=2)
    year = serializers.CharField(max_length=2, min_length=2)
