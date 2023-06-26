from rest_framework import serializers
from .models import Category, Subcategory
from product_api.models import Product, Review


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
    

class PopularProductSerializer(serializers.ModelSerializer):   
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 
            'count', 'date', 'title',
            'description', 'freeDelivery', 'images',
            'tags', 'reviews', 'rating']
        
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
        

class LimitedProductSerializer(serializers.ModelSerializer):   
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 
            'count', 'date', 'title',
            'description', 'freeDelivery', 'images',
            'tags', 'reviews', 'rating']
        
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
        

class BannersSerializer(serializers.ModelSerializer):   
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 
            'count', 'date', 'title',
            'description', 'freeDelivery', 'images',
            'tags', 'reviews', 'rating']
        
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
        