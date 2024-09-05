from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets

from .permissions import (
    IsAdminOrReadOnlyPermission,
    IsAuthorOrReadOnlyPermission
)

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    TitlesWriteSerializer,
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
    filter_backends = [filters.SearchFilter]
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
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)
    permission_classes = IsAdminOrReadOnlyPermission,
    pagination_class = CustomPaginator


class TitlesViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""   
    serializer_class = TitlesSerializer
    permission_classes = IsAdminOrReadOnlyPermission,
    pagination_class = CustomPaginator
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = (
            Titles.objects.all()
            .annotate(rating=Avg('reviews__score'))
            .order_by('name')
        )
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name=name)
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__slug=genre)
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializer
        return TitlesWriteSerializer


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
