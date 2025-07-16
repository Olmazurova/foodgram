from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from .constants import MAX_LENGTH


class User(AbstractUser):
    """Модель пользователя с дополнительным полем avatar."""

    email = models.EmailField(
        verbose_name='Email', max_length=MAX_LENGTH, unique=True
    )
    # password = models.CharField(verbose_name='пароль', max_length=MAX_LENGTH)
    avatar = models.ImageField(
        verbose_name='аватар',
        upload_to='media/users/',
        default=None,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
