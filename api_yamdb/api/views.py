from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets

from .permissions import IsAdminOrReadOnlyPermission, IsAuthorOrReadOnlyPermission

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer,
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
    # Добавила вычесление и включение средней оценки для каждого объекта Title.
    queryset = (
        Titles.objects.all()
        .annotate(rating=Avg('reviews__score'))
        .order_by('name')
    )

    serializer_class = TitlesSerializer
    permission_classes = IsAdminOrReadOnlyPermission,
    pagination_class = CustomPaginator
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    ordering_fields = ('name', 'year')
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']


class ReviewsViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""

    queryset = Reviews.objects.all()
    permission_classes = IsAuthorOrReadOnlyPermission,
    serializer_class = ReviewSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        """Переопределение получения класса ReviewViewSet."""
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение создания класса ReviewViewSet."""
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)




class CommentsViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    queryset = Comments.objects.all()
    permission_classes = IsAuthorOrReadOnlyPermission,
    serializer_class = CommentSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
