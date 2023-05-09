from rest_framework import serializers

from reviews.models import User, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
