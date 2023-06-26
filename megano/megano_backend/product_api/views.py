from django.shortcuts import render
from .models import Product
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductRetrievApiView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category', 'specifications').prefetch_related('tags', 'image', 'reviews').all()
