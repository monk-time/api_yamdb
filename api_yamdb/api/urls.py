from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthTokenView,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    SignUpView,
    TitleViewSet,
    UserViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review',
)

auth_urls = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', AuthTokenView.as_view(), name='auth_token'),
]

api_v1_urls = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_urls)),
]

urlpatterns = [
    path('v1/', include(api_v1_urls)),
]
