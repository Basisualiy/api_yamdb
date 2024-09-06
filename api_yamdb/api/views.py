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
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Category, Genre, Title, Review, Comments
from users.views import CustomPaginator


class CategoriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
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

    queryset = Genre.objects.all()
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
        """Добавляем возможность фильтрации по query_params."""
        queryset = (
            Title.objects.all()
            .annotate(rating=Avg('review__score'))
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
        """Выбираем сериализатор для создания или получения произведения."""
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializer
        return TitlesWriteSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    queryset = Review.objects.all()
    permission_classes = IsAuthorOrReadOnlyPermission,
    serializer_class = ReviewSerializer
    pagination_class = CustomPaginator
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Переопределение получения класса ReviewViewSet."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение создания класса ReviewViewSet."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comments.objects.all()
    permission_classes = IsAuthorOrReadOnlyPermission,
    serializer_class = CommentSerializer
    pagination_class = CustomPaginator
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Получаем отзывы для текущего произведения."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохраняем текущего пользователя как автора произведения."""
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
