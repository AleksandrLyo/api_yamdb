from os import listdir
from os.path import exists, isfile, join, splitext
from pathlib import Path

from django.apps import apps
from django.conf import settings


def get_path(options):
    input_path = Path(options['path'])
    path = join(settings.BASE_DIR, input_path)
    print(f'Введена директория: {path}')
    if exists(path):
        print('Директория найдена...')
        return path
    else:
        raise FileNotFoundError('Директория НЕ найдена!')


def get_files(path):
    files_dict = {
        'category': 'category.csv',
        'comment': 'comments.csv',
        'genre': 'genre.csv',
        'title_genre': 'genre_title.csv',
        'review': 'review.csv',
        'title': 'titles.csv',
        'users': 'users.csv',
    }
    access_files = {}
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    for model_name, files in files_dict.items():
        if files in files_list:
            print(f'Для модели {model_name} найден файл {files}')
            access_files[model_name] = files
        else:
            print(f'*Для модели {model_name} файл НЕ найден!')
    if not access_files:
        raise TypeError('Не найденно ни одного подходящего файла')
    return access_files


def load_data(files, path):

    models = {**apps.all_models['reviews'], **apps.all_models['users']}
    for model_name, file in files.items():
        if model_name in models:
            model = models[model_name]
            file_path = join(path, file)
            with open(file_path) as csv_file:
                pass

    # files_name_list = [splitext(name) for name in files_list]