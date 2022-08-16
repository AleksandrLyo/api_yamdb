from django.core.management import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Загрузка данных из csv-файлов"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'path',
            type=str,
            help='Путь к папке с csv файлами'
        )

    def handle(self, *args, **options):
        self.stdout.write('Тестовая команда')
        path = os.path.join(
            settings.BASE_DIR,
            options['path']
        )
        if os.path.exists(path)
        self.stdout.write(str(path))
