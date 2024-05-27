import csv
import sys
from dataclasses import dataclass, field

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model

from reviews.models import Category, Comment, Genre, Review, Title, User

BASE_DIR = settings.STATICFILES_DIRS[0] / 'data'


@dataclass
class CSVModel:
    filename: str
    model: Model
    mapping: dict[str, str] = field(default_factory=dict)

    def mapped(self, row: dict) -> dict:
        for key, new_key in self.mapping.items():
            if key in row:
                row[new_key] = row.pop(key)
        return row

    def load(self):
        try:
            with (BASE_DIR / self.filename).open(encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.model.objects.bulk_create(
                    self.model(**self.mapped(row)) for row in reader
                )
        except FileNotFoundError as e:
            msg = f'File {self.filename} not found'
            raise CommandError(msg) from e


CATEGORY_MAPPING = {'category': 'category_id'}
AUTHOR_MAPPING = {'author': 'author_id'}

CSV_MODELS = (
    CSVModel(filename='users.csv', model=User),
    CSVModel(filename='category.csv', model=Category),
    CSVModel(filename='genre.csv', model=Genre),
    CSVModel(filename='titles.csv', model=Title, mapping=CATEGORY_MAPPING),
    CSVModel(filename='review.csv', model=Review, mapping=AUTHOR_MAPPING),
    CSVModel(filename='comments.csv', model=Comment, mapping=AUTHOR_MAPPING),
    CSVModel(filename='genre_title.csv', model=Title.genre.through),
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.stdout.write(
            self.style.MIGRATE_HEADING('Loading into database:\n')
        )
        for csv_model in CSV_MODELS:
            sys.stdout.write(
                f'  Loading model {csv_model.model.__name__} '
                f'from {csv_model.filename}...'
            )
            csv_model.load()
            sys.stdout.write(self.style.SUCCESS(' OK\n'))
