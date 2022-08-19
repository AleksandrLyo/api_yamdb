
from . utils import get_path, get_files, load_data


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
        path = get_path(options)
        files = get_files(path)
        print(files)
        load_data(files, path)
        



