from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH, User
from .validators import validate_username_not_me

USER_FIELDS = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username_not_me],
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()
        if not any((user_by_username, user_by_email)):
            return User.objects.create(**validated_data)
        if user_by_username == user_by_email:
            return user_by_username
        response = {}
        if user_by_username:
            response['username'] = ['Already used']
        if user_by_email:
            response['email'] = ['Already used']
        raise ValidationError(response)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_FIELDS


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = USER_FIELDS
        read_only_fields = ('role',)
