from django.urls import include, path
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path('v1/auth/', include('custom_auth.urls')),
]