from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone

from .validators import PhoneNumberValidator
from .messages import UserMessage

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=14,
        unique=True,
        help_text=UserMessage.PHONE_NUMBER_HELP_TEXT.value,
        validators=[PhoneNumberValidator],
    )
    username = models.CharField(max_length=200, blank=True, default='')
    first_name = models.CharField(max_length=200, blank=True, default='')
    last_name = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(default='', blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
