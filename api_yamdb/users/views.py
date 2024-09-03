from django.contrib.auth import get_user_model
from rest_framework import exceptions, filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import IsAdminPermission
from .serializer import UsersSerializer

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = IsAdminPermission,
    filter_backends = filters.SearchFilter,
    search_fields = 'username',
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = LimitOffsetPagination


@api_view(http_method_names=['GET', 'PATCH'])
def me(request):
    if request.auth:
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = UsersSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
    raise exceptions.NotAuthenticated()
