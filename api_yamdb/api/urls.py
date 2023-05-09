from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthTokenView,
    SignUpView,
    UserViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
)

router_v1 = DefaultRouter()

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', AuthTokenView.as_view(), name='auth_token'),
    path('v1/', include(router_v1.urls)),
]
