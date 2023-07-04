from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from product_api.models import Product
from .serializers import BasketSerializer
    
class BasketApiView(ListAPIView):
    serializer_class = BasketSerializer
    
    def data(self):
        queryset = self.get_queryset()
        serializer = BasketSerializer(queryset, context = self.request.session['cart'], many=True)
        return serializer.data
    
    def get_queryset(self):
        products = self.request.session['cart']
        ids = list()
        for i in products:
            ids.append(i['id'])
        data = Product.objects.select_related('category').prefetch_related('image').filter(id__in=ids)
        return data
    
    def delete(self, request):
        product_id = request.data['id']
        count = int(request.data['count'])
        for index, value in enumerate(request.session['cart']):
                if next(iter(value.values())) == product_id:
                    request.session['cart'][index]['count'] -= count
                    if request.session['cart'][index]['count'] == 0:
                        request.session['cart'].remove(request.session['cart'][index])
                    request.session.save()                    
                    return Response(self.data())
        return Response(status=500)
    
    def get(self, request):
        return Response(self.data())
    
    def post(self, request):
        product_id = request.data['id']
        count = int(request.data['count'])
        if  'cart' in request.session:          
            for index, value in enumerate(request.session['cart']):
                if next(iter(value.values())) == product_id:
                    request.session['cart'][index]['count'] += count
                    request.session.save()
                    return Response(self.data())
            request.session['cart'].append({'id': product_id, 'count': count})
            request.session.save()
            return Response(self.data())
        request.session['cart'] = [{'id': product_id, 'count': count}]
        request.session.save()
        return Response(self.data())