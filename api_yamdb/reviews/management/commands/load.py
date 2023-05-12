import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_models = (
            ("users.csv", User),
            ("category.csv", Category),
            ("genre.csv", Genre),
            ("titles.csv", Title),
            ("review.csv", Review),
            ("comments.csv", Comment),
            ("genre_title.csv", None),
        )
        for file_name, model in csv_models:
            try:
                with open(
                    settings.STATICFILES_DIRS[0] / "data" / file_name,
                    encoding="utf-8",
                ) as csvfile:
                    reader = csv.DictReader(csvfile)
                    if file_name == "genre_title.csv":
                        for row in reader:
                            title = Title.objects.get(id=row["title_id"])
                            genre = Genre.objects.get(id=row["genre_id"])
                            title.genre.add(genre)
                    else:
                        for row in reader:
                            for key in ("category", "author"):
                                if key in row:
                                    value = row.pop(key)
                                    row[f"{key}_id"] = value
                            model.objects.create(**row)
            except FileNotFoundError:
                raise CommandError(f"Файл {file_name} не найден")
