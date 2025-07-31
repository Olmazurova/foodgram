import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к csv-файлу.'
        )

    def handle(self, *args, **options):
        file_path = options.get('file_path')

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            for row in reader:
                name, unit = row
                Ingredient.objects.create(
                    name=name.strip(), measurement_unit=unit.strip()
                )
                count += 1

            self.stdout.write(
                self.style.SUCCESS(f'Всего загружено {count} ингредиентов.')
            )
