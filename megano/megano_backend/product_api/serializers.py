from rest_framework import serializers
from .models import Category, Subcategory, Product, Review, Tags


class SubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': obj.image.name,
        }


class CatalogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        return {
            'src': obj.images.url,
            'alt': obj.images.name,
        }


class SaleSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'price', 'salePrice',
            'dateFrom', 'dateTo',
            'title', 'images']

    def get_images(self, obj):
        return [{
            'src': image.image.url,
            'alt': image.image.name
        }
            for image in obj.image.all()
        ]


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'salePrice',
                  'dateFrom', 'dateTo',
                  'count', 'date', 'title', 'description', 
                  'fullDescription', 'freeDelivery', 'images', 
                  'tags', 'reviews', 'specifications', 'rating']
        
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
    
    def get_tags(self, obj):
        return [
            {'name' : tag.name,
             'id': tag.id}
            for tag in obj.tags.all()
        ]
    
    def get_specifications(self, obj):
        specifications = obj.specifications.all()
        if specifications:
            return [
                {
                    'name': specification.name,
                    'value': specification.value
                }
                for specification in specifications
            ]
        return []
        
    def get_reviews(self, obj):
        return [
            {
                'author': review.author.username,
                'email': review.author.profile.email,
                'text': review.text,
                'rate': review.rate,
                'date': review.date
            }
            for review in obj.reviews.all()
            if review.checked
        ]
        
    def get_rating(self, obj):
        rate_points = [ review.rate for review in Review.objects.filter(product=obj)]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            return rating
        return 0
        