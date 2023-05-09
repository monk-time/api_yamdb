from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_username_not_me


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


class Title(models.Model):
    pass

# нужно предусмотреть чтобы один пользователь
# может оставить один отзыв
class Review(models.Model):
    author = models.ForeignKey(
        # verbose_name='Автор отзыва',
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        # 'Произведение',
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        # 'Текст отзыва',
    )
    score = models.IntegerField(
        'Оценка от 1 до 10(обязательно)',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публиции отзыва',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return self.text[:15]

# Это заготовка для feature/comments.
# 
# class Comment(models.Model):
#     author = models.ForeignKey(
#         'Автор комментария',
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments',
#     )
#     review = models.ForeignKey(
#         'Отзыв',
#         Review,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     text=models.TextField(
#         'Текст комментария',
#     )
#     comment_date = models.DateTimeField(
#         'Дата публиции комментария',
#         auto_now_add=True,
#     )

#     class Meta:
#         ordering = ('-comment_date',)
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
    
#     def __str__(self):
#         return self.text[:15]

