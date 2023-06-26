from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

class OrderRetrieveUpdateApiView(RetrieveUpdateAPIView):
    
    def get(self, request):
        print(request.data)
        return Response(status=500)
    
    def post(self, request):
        print(request.data)
        return Response(status=500)
        
