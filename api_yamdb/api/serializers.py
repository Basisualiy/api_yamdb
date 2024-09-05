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
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['rating'] = instance.rating
        except AttributeError:
            pass
        return data


class TitlesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genres.objects.all())

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

    def create(self, validated_data):
        try:
            genres = validated_data.pop('genre')
        except KeyError:
            raise exceptions.ValidationError(code=status.HTTP_400_BAD_REQUEST)
        title = Titles.objects.create(**validated_data)
        if isinstance(genres, list) or isinstance(genres, tuple):
            for genre in genres:
                title.genre.add(genre)
                title.save()
        else:
            title.genre.add(get_object_or_404(Genres, slug=genres))
            title.save()
        return title


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
