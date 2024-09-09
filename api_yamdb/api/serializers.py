import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers, status
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comments

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, attrs):
        try:
            email = self.initial_data['email']
            username = self.initial_data['username']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        if username == 'me':
            raise exceptions.ValidationError(
                f'Имя - {username} запрещено использовать для регистрации',
                code=status.HTTP_400_BAD_REQUEST)
        if re.match('^[\\w.@+-]+\\Z', username) is None:
            raise exceptions.ValidationError(
                'Имя пользователя не соответствует шаблону',
                code=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(username=username).first()
        if user and user.email != email:
            raise exceptions.ValidationError(
                f'Пользователь с username = {username} уже зарегистрирован',
                code=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user and user.username != username:
            raise exceptions.ValidationError(
                f'Пользователь с email = {email} уже зарегистрирован',
                code=status.HTTP_400_BAD_REQUEST)
        return super().validate(attrs)


class TokenSerializator(serializers.ModelSerializer):
    """Сериализатор для авторизации пользователя и выдачи ему токена."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        try:
            username = data['username']
            confirmation_code = data['confirmation_code']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User, username=username)
        if user.confirmation_code != confirmation_code:
            raise exceptions.ValidationError('Неверный код подтверждения.',
                                             code=status.HTTP_400_BAD_REQUEST)
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователем."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
        max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(UsersSerializer):
    """Сериализатор для работы пользователя со своими данными."""
    role = serializers.CharField(read_only=True)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        exclude = 'id',


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = 'id',


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
        )


class TitlesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания произведения."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Reviews."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        """Валидация отзыва."""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data

    class Meta:
        """Мета класс для ReviewsSerializer."""

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Мета класс для CommentSerializer."""

        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
