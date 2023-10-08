"""Создание пользовательской команды импорта данных в БД из CSV-файлов."""

import csv
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser

CSV_MODELS_FIELDS = {
    CustomUser: ('users.csv', None, None),
    Category: ('category.csv', None, None),
    Genre: ('genre.csv', None, None),
    Title: ('titles.csv', 'category_id', 'category'),
    GenreTitle: ('genre_title.csv', None, None),
    Review: ('review.csv', 'author_id', 'author'),
    Comment: ('comments.csv', 'author_id', 'author')
}
path_to_csv_directory = os.path.join(BASE_DIR, 'static/', 'data/')


class Command(BaseCommand):
    """Класс импорта данных в БД из CSV-файлов."""

    def handle(self, *args, **options):
        """Функция фактической логики импорта данных в БД из CSV-файлов."""

        def csv_to_db(model, csv_file, csv_file_path):
            """Чтение файлов csv и добавление данных из них в БД."""
            with open(csv_file_path, 'r', encoding='utf-8') as data_csv_file:
                reader = csv.DictReader(data_csv_file)
                _, db_field, scv_field = CSV_MODELS_FIELDS[model]
                for row in reader:
                    if scv_field:
                        row[db_field] = row.pop(scv_field)
                    model.objects.create(**row)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные из файла {csv_file} успешно импортированы'
                        f' в таблицу БД {model.__name__}.'
                    )
                )
        for model, (csv_file, _, _) in CSV_MODELS_FIELDS.items():
            csv_file_path = Path(path_to_csv_directory) / csv_file
            csv_to_db(model, csv_file, csv_file_path)
