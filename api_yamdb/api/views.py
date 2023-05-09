from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User, Title, Review
from .permissions import (
    IsAdminOrSuper,
    IsAdminOrReadOnly,
    IsStaffOrAuthorOrReadOnly,
)
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
    ReviewSerializer,
)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_confirmation_code(token: str, email: str):
        send_mail(
            subject='Код подтверждения для API YaMDb',
            message=f'Ваш код подтверждения: {token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, User):
            user = serializer.validated_data
        else:
            user = serializer.save()

        token = default_token_generator.make_token(user)
        self.send_confirmation_code(token, user.email)
        return Response(serializer.data)


class AuthTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                {"confirmation_code": ["Код подтверждения неверный"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = AccessToken.for_user(user)
        return Response({'token': str(access_token)})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuper,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)  # нужно будет проверить
    pagination_class = PageNumberPagination

    def title_get(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_get'),
        )

    def get_queryset(self):
        return self.title_get().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.title_get(),
        )
