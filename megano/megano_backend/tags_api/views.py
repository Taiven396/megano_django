from rest_framework.generics import ListAPIView
from .models import Tags
from .serializers import TagsSerializers


class TagsListApiView(ListAPIView):
    model = Tags
    serializer_class = TagsSerializers
    queryset = Tags.objects.all()
