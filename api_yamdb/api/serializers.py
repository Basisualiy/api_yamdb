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
        model = Titles
        fields = (
            'id',
            'category',
            'genre',
            'name',
            'year',
            'description'
        )


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

    # Уникальность отзывов на одно произведение.
    def validate(self, data):
        title_id = self.context['title_id']
        if self.context['request'].method == 'POST' and Reviews.objects.filter(
            title=title_id, author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.')
        return data

    def create(self, validated_data):
        return Reviews.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        model = Comments
        fields = ('id', 'review', 'author', 'text', 'pub_date')

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)
