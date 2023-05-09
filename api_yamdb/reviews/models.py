from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import validate_username_not_me, validate_year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_not_me,
        ],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
    )

    class Meta:
        ordering = ['id']

    @property
    def is_admin_or_super(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Genre(models.Model):
    '''Модель жанра произведения'''

    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    '''Модель категории произведения'''

    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Модель названия произведения'''

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.IntegerField(
        validators=[validate_year], verbose_name='Год выпуска'
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
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


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
