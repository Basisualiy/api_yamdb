from django.urls import include, path
from rest_framework.routers import DynamicRoute, Route, SimpleRouter
from . import views


class UsersRouter(SimpleRouter):
    routes = [
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
    ]


users_router = UsersRouter()
users_router.register('', views.UsersViewSet)


router = SimpleRouter()
router.register('titles', views.TitlesViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet, basename='comments')
router.register('genres', views.GenresViewSet, basename='genres')
router.register('categories', views.CategoriesViewSet, basename='categories')

auth_urls = [
    path('signup/', views.SignUpViewSet.as_view(), name='signup'),
    path('token/', views.TokenApiView.as_view(), name='token'),
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/users/', include(users_router.urls)),
    path('v1/auth/', include(auth_urls)),
]
