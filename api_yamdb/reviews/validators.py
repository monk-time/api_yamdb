from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя "me" использовать нельзя')


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            'Некорретный год публикации произведения.'
            f'{year} больше текущего года'
        )
