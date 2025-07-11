from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import MAX_LENGTH

class User(AbstractUser):
    """Модель пользователя с дополнительным полем avatar."""

    email = models.EmailField(
        verbose_name='Email', max_length=MAX_LENGTH, unique=True
    )
    password = models.CharField(verbose_name='password', max_length=MAX_LENGTH)
    avatar = models.ImageField(verbose_name='аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # is_subscribed - в сериализаторе
