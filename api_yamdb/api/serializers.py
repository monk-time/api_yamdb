from django.db.models import Avg
from rest_framework import serializers, validators

from reviews.models import Category, Comment, Genre, Review, Title, User


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
        read_only_fields = ('role',)


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


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор названия произведения для POST и PATCH методов."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    # rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    # def get_rating(self, obj):
    #     return obj.reviews.aggregate(rating=Avg('score'))['rating']


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор названия произведения для GET методов."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    # rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    # def get_rating(self, obj):
    #     return obj.reviews.aggregate(rating=Avg('score'))['rating']


# нужно предусмотреть чтобы один пользователь
# может оставить один отзывf
class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для Отзывов"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    # title = serializers.PrimaryKeyRelatedField(
    #     read_only=True,
    #     default=serializers.CurrentUserDefault(),
    # )

    class Meta:  # попробовать exclude title
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            # 'title',
        )
        # validators = [
        #     validators.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('author','title'),
        #         message='Нельзя оставлять отзыв дважды на одно и тоже произвдение',
        #     )            
        # ]

    # def validate_author(self, value):
    #     if self.context['request'].author == value:
    #         raise serializers.ValidationError(
    #             "Нельзя оставлять отзыв дважды на одно и тоже произвдение"
    #         )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Комментариев"""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:  # попробовать exclude review
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
