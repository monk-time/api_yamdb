from rest_framework import serializers

from reviews.models import Сategory, Genre, Title


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
