from django.db import models
from django.contrib.auth.models import User


def avatar_upload_path(instanse, filename):
    return f"avatars/user_{instanse.user.id}/{filename}"


class Profile(models.Model):
    fullName = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username
