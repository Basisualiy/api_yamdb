from django.urls import path

from .views import SignUpViewSet, TokenApiView

app_name = 'auth'

urlpatterns = [
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path('token/', TokenApiView.as_view(), name='token'),
]
