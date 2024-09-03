from django.urls import include, path
from rest_framework.routers import SimpleRouter

# Import your app views
from .views import TitlesViewSet, ReviewsViewSet, CommentsViewSet, GenresViewSet, CategoriesViewSet

# Create a router and register your viewsets
router = SimpleRouter()
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')
router.register( r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet, basename='comments')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'categories', CategoriesViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/users/', include('users.urls')),
    path('v1/auth/', include('custom_auth.urls')),
]
