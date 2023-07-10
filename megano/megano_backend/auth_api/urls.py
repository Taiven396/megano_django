from django.urls import path
from .views import (
    SignInApiView,
    SignOutApi,
    SignUpCreateApiView,
    ProfileRetrievUpdateView,
    ProfileAvatarUpdateView,
    PasswordApiView
    ) 

app_name = 'auth_api'

urlpatterns = [
    path('sign-in', SignInApiView.as_view(), name='sign-in'),
    path('sign-up', SignUpCreateApiView.as_view(), name='sign-up'),
    path('sign-out', SignOutApi.as_view(), name='sign-out'),
    path('profile', ProfileRetrievUpdateView.as_view(), name='profile'),
    path('profile/avatar', ProfileAvatarUpdateView.as_view(), name='profile-avatar'),
    path('profile/password', PasswordApiView.as_view(), name='profile-password'),
]