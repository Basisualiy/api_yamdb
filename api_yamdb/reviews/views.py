from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from reviews.models import Categories, Genres, Titles, Reviews, Comments
from api.serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    ReviewsSerializer,
    CommentsSerializer,
)


class CategoriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter)
    search_fields = ('name')


class GenresViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для жанров."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter)
    search_fields = ('name')


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    ordering_fields = ('name', 'year')


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
