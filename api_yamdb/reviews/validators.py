from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            'Некорретный год публикации произведения.'
            f'{year} больше текущего года'
        )
