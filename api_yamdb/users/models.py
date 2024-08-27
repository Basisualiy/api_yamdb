from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUser(AbstractUser):
    role = models.CharField('Роль пользователя',
                            max_length=15,
                            choices=ROLES,
                            default='user')
    bio = models.CharField('Биография',
                           max_length=1024,
                           blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
