from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnlyPermission
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    ReviewsSerializer,
    CommentsSerializer,
)
from reviews.models import Categories, Genres, Titles, Reviews, Comments
from users.views import CustomPaginator


class CategoriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий."""

    queryset = Categories.objects.all()
    permission_classes = IsAdminOrReadOnlyPermission,
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)
    pagination_class = CustomPaginator


class GenresViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для жанров."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    # Добавила вычесление и включение средней оценки для каждого объекта Title.
    queryset = (
        Titles.objects.all().annotate(Avg('reviews__score')).order_by('name')
    )

    serializer_class = TitlesSerializer
    pagination_class = CustomPaginator
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    ordering_fields = ('name', 'year')


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = CustomPaginator


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        """
        Возвращаем комментарии, связанные с указанным отзывом,
        используя параметры из URL.
        """
        review = get_object_or_404(
            Reviews.objects.filter(title_id=self.kwargs.get('title_id')),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        """
        Сохраняем новый комментарий,
        связывая его с отзывом и текущим пользователем.
        """
        review = get_object_or_404(
            Reviews.objects.filter(title_id=self.kwargs.get('title_id')),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
