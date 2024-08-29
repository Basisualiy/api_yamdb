from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.validators import validate_username
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для получение кода подтверждения."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получение JWT-токена."""
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

def validate(self, data):
    user = get_object_or_404(User, username=data['username'])
    if user.confirmation_code != data.get('confirmation_code'):
        raise serializers.ValidationError('Не верный confirmation_code')
    return {'access': str(AccessToken.for_user(user))}
