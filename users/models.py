from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    CURRENCY_CHOICES = [
        ('PEN', 'Sol Peruano'),
        ('USD', 'Dólar'),
        ('EUR', 'Euro'),
    ]

    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    preferred_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='PEN'
    )

    ui_language = models.CharField(
        max_length=2,
        choices=[
            ('es', 'Spanish'),
            ('en', 'English'),
        ],
        default='es'
    )

    ui_theme = models.CharField(
        max_length=5,
        choices=[
            ('dark', 'Dark'),
            ('light', 'Light'),
        ],
        default='dark'
    )

    timezone = models.CharField(
        max_length=50,
        default='America/Lima'
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
