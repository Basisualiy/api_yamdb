from django.contrib.auth import get_user_model
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.permissions import IsAdminPermission
from .serializer import MeSerializer, UsersSerializer

User = get_user_model()


class CustomPaginator(PageNumberPagination):
    page_size = 10


class UsersViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'options', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = IsAdminPermission,
    filter_backends = filters.SearchFilter,
    search_fields = 'username',
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    pagination_class = CustomPaginator


@api_view(http_method_names=['GET', 'PATCH'])
def me(request):
    if request.auth:
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    raise exceptions.NotAuthenticated()
