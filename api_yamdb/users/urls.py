from django.urls import include, path
from rest_framework.routers import SimpleRouter

users_router = SimpleRouter()


urlpatterns = [
    path('', include(users_router.urls))
]