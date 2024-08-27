from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
        validators=[validators.RegexValidator(r'^[\w.@+-]+\Z'),])
    email = models.EmailField('email пользователя',
                              max_length=254,
                              unique=True)
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 blank=True)
    role = models.CharField('Роль пользователя',
                            max_length=15,
                            choices=ROLES,
                            default='user')
    bio = models.TextField('Биография',
                           blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
