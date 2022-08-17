from os import listdir
from os.path import exists, isfile, join, splitext
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Загрузка данных из csv-файлов"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'path',
            type=str,
            help='Путь к папке с csv файлами'
        )

    def handle(self, *args, **options):
        print('Тестовая команда')
        input_path = Path(options['path'])
        path = join(
            settings.BASE_DIR,
            input_path
        )
        self.stdout.write('Введена директория:')
        self.stdout.write(str(path))
        if exists(path):
            self.stdout.write('Директория найдена...')
        else:
            raise FileNotFoundError('Директория НЕ найдена!')
        self.stdout.write('Поиск файлов по названию таблиц...')
        # apps.all_models['']
        files_list = [f for f in listdir(path) if isfile(join(path, f))]
        print(files_list)
        
