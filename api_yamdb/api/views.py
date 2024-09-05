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
