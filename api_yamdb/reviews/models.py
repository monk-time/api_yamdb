from django.db import models

from .validations import validate_year


class Genre(models.Model):
    '''Модель жанра произведения'''

    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Сategory(models.Model):
    '''Модель категории произведения'''

    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель названия произведения'''

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(
        validators=validate_year, verbose_name='Год выпуска'
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug жанра',
        help_text='Жанр, к которому будет относиться произведение',
    )
    category = models.ForeignKey(
        Сategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug категории',
        help_text='Категория, к которому будет относиться произведение',
    )

    class Meta:
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name
