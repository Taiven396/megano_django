from django.urls import path
from .views import (
    PasswordApiView,
    ProfileRetrievUpdateView,
    ProfileAvatarUpdateView
)


app_name = 'profile_api'

urlpatterns = [
    path('profile', ProfileRetrievUpdateView.as_view(), name='profile'),
    path('profile/avatar', ProfileAvatarUpdateView.as_view(), name='profile-avatar'),
    path('profile/password', PasswordApiView.as_view(), name='profile-password')
]