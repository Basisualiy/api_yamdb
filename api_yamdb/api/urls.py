from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SignUpViewSet, TokenViewSet

app_name = 'api'

router_v1 = SimpleRouter()

auth_urls = [
    path(
        'signup/', SignUpViewSet.as_view(), name='signup',
    ),
    path(
        'token/', TokenViewSet.as_view(), name='token'
    )
]
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
