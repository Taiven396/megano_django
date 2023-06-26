from django.urls import path
from .views import (
    SignInApiView,
    SignOutApi,
    SignUpCreateApiView
    ) 

app_name = 'auth_api'

urlpatterns = [
    path('sign-in', SignInApiView.as_view(), name='sign-in'),
    path('sign-up', SignUpCreateApiView.as_view(), name='sign-up'),
    path('sign-out', SignOutApi.as_view(), name='sign-out')
]