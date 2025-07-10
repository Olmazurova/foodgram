from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import MAX_LENGTH

class User(AbstractUser):
    """Модель пользователя с дополнительным полем avatar."""

    email = models.EmailField(verbose_name='Email', max_length=MAX_LENGTH)
    password = models.CharField(verbose_name='password')
    avatar = models.ImageField(verbose_name='аватар')
    # is_subscribed - в сериализаторе
