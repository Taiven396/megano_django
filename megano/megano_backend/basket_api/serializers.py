from product_api.models import Product, Review
from rest_framework import serializers


class BasketSerializer(serializers.ModelSerializer):   
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    
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
        rate_points = [ review.rate for review in Review.objects.filter(product=obj).all()]
        if len(rate_points) > 0:
            rating = sum(rate_points) / len(rate_points)
            return rating
        return 0
    
    def get_tags(self, obj):
        tags = [ tag.name for tag in obj.tags.all()]
        print(tags)
        return [
            tag.name
            for tag in obj.tags.all()
        ]      