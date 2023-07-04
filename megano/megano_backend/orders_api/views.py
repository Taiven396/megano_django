from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from  .models import Order, OrderProduct
from  .serializers import OrderSerializer
from  product_api.models import Product
from django.core.exceptions import PermissionDenied

    
class OrderListApiView(ListAPIView):
    model = Order
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            'products_in_order').filter(customer=self.request.user)
        return queryset

    def post(self, request):
        total_cost = 0
        for product in request.data:
            cost = float(product['price']) * int(product['count'])
            total_cost += cost
        order = Order.objects.create(
            totalCost = total_cost
        )
        for i_product in request.data:
            product = Product.objects.get(id=i_product['id'])
            OrderProduct.objects.create(
                order = order,
                product = product,
                count = i_product['count']
            )
        request.session['cart'] = []
        print(order.id)
        data = {'orderId': order.id}
        request.session['orderId'] = order.id
        return Response(status=200, data=data)

            

class OrderRetrieveApiView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related('products_in_order').all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object.customer:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
        

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=request.data['orderId'])
        order.city = request.data['city']
        order.address = request.data['address']
        order.paymentType = request.data['paymentType']
        order.deliveryType = request.data['deliveryType']
        order.status = 'created'
        order.save()
        data = {
            'orderId': order.id
        }
        return Response(status=200, data=data)


class PaymentRetrieveApiView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.prefetch_related('products_in_order').all()
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['pk'])
        print(order.address)
        print(request.data)
        print(args)
        print(kwargs)
        return Response(status=200) 