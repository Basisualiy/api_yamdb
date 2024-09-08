from rest_framework import filters, mixins

from .paginators import CustomPaginator
from .permissions import IsAdminOrReadOnlyPermission


class BaseMixin(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,):

    permission_classes = IsAdminOrReadOnlyPermission,
    pagination_class = CustomPaginator


class GenreAndCategoryMixin(BaseMixin):
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleReviewsCommentsMixin():
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = CustomPaginator
