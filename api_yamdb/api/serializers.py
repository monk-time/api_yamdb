from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий произведения."""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра произведения."""

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведения для записи."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведения для чтения."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(author=request.user).exists():
                raise validators.ValidationError(
                    'Нельзя оставлять отзыв дважды на одно и тоже произвдение'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Комментариев"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        exclude = ('review',)
