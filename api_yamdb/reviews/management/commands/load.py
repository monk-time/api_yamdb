import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_models = (
            ('users.csv', User),
            ('category.csv', Category),
            ('genre.csv', Genre),
            ('titles.csv', Title),
            ('review.csv', Review),
            ('comments.csv', Comment),
            ('genre_title.csv', Title.genre.through),
        )
        for file_name, model in csv_models:
            try:
                path = settings.STATICFILES_DIRS[0] / 'data' / file_name
                with open(path, encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        for key in ('category', 'author'):
                            if key in row:
                                row[f'{key}_id'] = row.pop(key)
                        model.objects.create(**row)
            except FileNotFoundError:
                raise CommandError(f'Файл {file_name} не найден')
