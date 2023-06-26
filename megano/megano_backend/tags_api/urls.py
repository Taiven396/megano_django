from django.urls import path
from .views import TagsListApiView

app_name = 'tags_api'

urlpatterns = [
    path('tags', TagsListApiView.as_view(), name='tags-api')
]