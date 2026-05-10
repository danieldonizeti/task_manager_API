from django.core.management.base import BaseCommand
from apps.categories.models import Category


SYSTEM_CATEGORIES = ['Trabalho', 'Pessoal', 'Estudos', 'Saúde', 'Finacças']

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for name in SYSTEM_CATEGORIES:
            Category.objects.get_or_create(name=name, user=None)
            self.stdout.write(f'OK: {name}')