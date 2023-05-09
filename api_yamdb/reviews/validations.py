from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            'Некорретный год публикации произведения.'
            f'{year} больше текущего года'
        )
