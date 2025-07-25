from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Удалить все ингредиенты из базы данных'

    def handle(self, *args, **options):
        count, _ = Ingredient.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f'Всего удалено ингредиентов: {count}')
        )
