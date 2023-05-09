from rest_framework import serializers

from reviews.models import Category, Genre, Title
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
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    '''Сериализатор категорий произведения.'''

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор жанра произведения.'''

    class Meta:
        fields = '__all__'
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    '''Сериализатор названия произведения для POST и PATH методов.'''

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


class TitleGetSerializer(serializers.ModelSerializer):
    '''Сериализатор названия произведения для GET методов.'''

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return sum(review.score for review in reviews) / len(reviews)
