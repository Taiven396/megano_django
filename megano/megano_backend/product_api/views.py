from .models import Product, Review
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from  django.contrib.auth.models import User
from  profile_api.models import  Profile


class ProductListApiView(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = queryset = Product.objects.select_related(
        'category', 'specifications').prefetch_related('tags', 'image', 'reviews').filter(id=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])
        try:
            user = User.objects.get(username=request.data['author'])
        except User.DoesNotExist:
            return Response(status=409)
        if user.username != request.user.username or user.profile.email != request.data['email']:
            return Response(status=409)
        Review.objects.create(
            author = user,
            text = request.data['text'],
            rate = request.data['rate'],
            product = product,
            checked = False
        )
        return Response(status=200)

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        serializer = ProductSerializer(data=self.get_queryset(), many=True)
        return super().get(request, *args, **kwargs)