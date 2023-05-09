from rest_framework import serializers

from reviews.models import Сategory, Genre, Title
from reviews.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def to_internal_value(self, data):
        email = data.get('email')
        username = data.get('username')

        if email and username:
            try:
                user = User.objects.get(email=email, username=username)
                return user
            except User.DoesNotExist:
                pass

        return super().to_internal_value(data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


USER_FIELDS = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_FIELDS


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_FIELDS

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


class CategoriesSerializer(serializers.ModelSerializer):
    '''Сериализатор категорий произведения.'''

    class Meta:
        model = Сategory


class GenresSerializer(serializers.ModelSerializer):
    '''Сериализатор жанра произведения.'''

    class Meta:
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    '''Сериализатор названия произведения.'''

    ...
