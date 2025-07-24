from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import MAX_LENGTH_EMAIL, MAX_LENGTH_CHARFIELD


class User(AbstractUser):
    """Модель пользователя с дополнительным полем avatar."""

    email = models.EmailField(
        verbose_name='Email', max_length=MAX_LENGTH_EMAIL, unique=True
    )
    first_name = models.CharField(
        _('first name'), max_length=MAX_LENGTH_CHARFIELD
    )
    last_name = models.CharField(
        _('last name'), max_length=MAX_LENGTH_CHARFIELD
    )
    avatar = models.ImageField(
        verbose_name='аватар',
        upload_to='users/',
        default=None,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
