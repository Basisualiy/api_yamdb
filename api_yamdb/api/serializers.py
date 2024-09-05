from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers, status
from reviews.models import Categories, Genres, Titles, Reviews, Comments


def instance_to_dict(instance, slug):
    obj = get_object_or_404(instance, slug=slug)
    return {'name': obj.name, 'slug': obj.slug}


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['rating'] = instance.rating
        except AttributeError:
            pass
        return data

    def create(self, validated_data):
        try:
            category = self.initial_data['category']
            genres = self.initial_data['genre']
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        if isinstance(genres, list) or isinstance(genres, tuple):
            validated_data['genre'] = [
                get_object_or_404(Genres, slug=genre)
                for genre in genres
            ]
        else:
            validated_data['genre'] = [get_object_or_404(
                Genres,
                slug=genres
            )]
        validated_data['category'] = get_object_or_404(
            Categories,
            slug=category
        )
        
        return super().create(validated_data)


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
        title = get_object_or_404(Titles, pk=title_id)
        if (
            request.method == 'POST'
            and Reviews.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError('Вы уже оставляли отзыв на это произведение.')
        return data

    class Meta:
        """Мета класс для ReviewsSerializer."""

        model = Reviews
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
        fields = ('id', 'text', 'author')
