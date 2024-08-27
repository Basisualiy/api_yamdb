import re

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Пользователь с таким именем '
                              'уже зарегистрирован')
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Недопустимые символы <{value}> .'),
        )


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Пользователь с такой почтой '
                              'уже зарегистрирован')
