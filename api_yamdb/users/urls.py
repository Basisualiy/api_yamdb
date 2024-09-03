from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import me, UsersViewSet

users_router = SimpleRouter()
users_router.register('', UsersViewSet)

urlpatterns = [
    path('me/', me, name='me'),
    path('', include(users_router.urls))
]
