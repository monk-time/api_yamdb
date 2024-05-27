from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    if value.lower() == 'me':
        msg = 'Имя пользователя "me" использовать нельзя'
        raise ValidationError(msg)
