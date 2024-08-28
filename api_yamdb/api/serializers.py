from rest_framework import serializers
from reviews.models import Categories, Genres, Titles, Reviews, Comments


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
        fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    class Meta:
        model = Reviews
        fields = (
            'id',
            'title',
            'author',
            'text',
            'score',
            'pub_date'
        )


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        model = Comments
        fields = ('id', 'review', 'author', 'pub_date')
