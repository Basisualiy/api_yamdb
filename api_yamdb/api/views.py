from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend


from . import serializers
from .filters import TitleFilter
from .mixins import GenreAndCategoryMixin, TitleReviewsCommentsMixin
from .paginators import CustomPaginator
from .permissions import (
    IsAdminPermission,
    IsAdminOrReadOnlyPermission,
    IsAuthorOrReadOnlyPermission
)
from .utils import get_confirmation_code

from reviews.models import Category, Genre, Title, Review


User = get_user_model()


class SignUpViewSet(APIView):
    """Регистрируем пользователя и высылаем ему код подтверждения."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        username = request.data.get('username', None)
        user = User.objects.filter(
            username=username, email=email
        ).first()
        if user is None:
            serializer = serializers.SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)
        confirmation_code = get_confirmation_code(user.email,
                                                  user.username)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(user.username,
                  f'Ваш код подтверждения: {confirmation_code}',
                  settings.SERVER_EMAIL,
                  [user.email, ],
                  fail_silently=False,)
        return Response(request.data,
                        status=status.HTTP_200_OK)


class TokenApiView(APIView):
    """Авторизуем пользователя и выдаем токен."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.TokenSerializator(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username'])
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({'confirmation_code': str(token.access_token)},
                        status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ModelViewSet):
    """Позволяет админу работать с пользователями."""
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = IsAdminPermission,
    filter_backends = filters.SearchFilter,
    search_fields = 'username',
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = CustomPaginator

    @action(detail=True, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated,])
    def me(self, request):
        """Позволяет пользователю изменить свои данные."""
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = serializers.MeSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = serializers.MeSerializer(user, data=request.data,
                                                  partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(
    GenreAndCategoryMixin,
    viewsets.GenericViewSet
):
    """ViewSet для категорий."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategoriesSerializer


class GenresViewSet(
    GenreAndCategoryMixin,
    viewsets.GenericViewSet
):
    """ViewSet для жанров."""

    queryset = Genre.objects.all()
    serializer_class = serializers.GenresSerializer


class TitlesViewSet(TitleReviewsCommentsMixin,
                    viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = (
        Title.objects.all()
        .annotate(rating=Avg('reviews__score'))
        .order_by('name')
    )
    serializer_class = serializers.TitlesSerializer
    permission_classes = IsAdminOrReadOnlyPermission,
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Выбираем сериализатор для создания или получения произведения."""
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitlesSerializer
        return serializers.TitlesWriteSerializer


class ReviewsViewSet(TitleReviewsCommentsMixin,
                     viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = serializers.ReviewSerializer
    permission_classes = IsAuthorOrReadOnlyPermission,

    def get_queryset(self):
        """Переопределение получения класса ReviewViewSet."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Переопределение создания класса ReviewViewSet."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(TitleReviewsCommentsMixin,
                      viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = serializers.CommentSerializer
    permission_classes = IsAuthorOrReadOnlyPermission,

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
