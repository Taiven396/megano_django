from rest_framework import serializers
from .models import Product, Review
from tags_api.models import Tags


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 
                  'count', 'date', 'title', 'description', 
                  'fullDescription', 'freeDelivery', 'images', 
                  'tags', 'reviews', 'specifications', 'rating']
        
        
    def get_images(self, obj):
        return [{
            'src': image.image.url,
            'alt': image.image.name
        }
             for image in obj.image.all()   
                ]
    
    def get_tags(self, obj):
        tags = [ tag.name for tag in obj.tags.all()]
        print(tags)
        return [
            tag.name
            for tag in obj.tags.all()
        ]
    
    def get_specifications(self, obj):
        specification = obj.specifications
        if specification:
            return [
                {
                    'name': specification.name,
                    'value': specification.value
                }
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
        ]
        
    def get_rating(self, obj):
        rate_points = [ review.rate for review in Review.objects.filter(product=obj).all()]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            return rating
        return 0
        