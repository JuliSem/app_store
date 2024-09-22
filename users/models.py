from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(
        verbose_name='Аватар',
        upload_to='users_images',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=10,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
