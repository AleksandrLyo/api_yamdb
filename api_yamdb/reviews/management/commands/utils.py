import csv
from os import listdir
from os.path import exists, isfile, join
from pathlib import Path

from django.apps import apps
from django.conf import settings

from ...models import Category, User


def get_path(options):
    input_path = Path(options['path'])
    path = join(settings.BASE_DIR, input_path)
    print(f'Введена директория: {path}')
    if exists(path):
        print('Директория найдена...')
        return path
    else:
        raise FileNotFoundError('Директория НЕ найдена!')


def check_files(path):
    files_dict = {
        'user': 'users.csv',
        'category': 'category.csv',
        'comment': 'comments.csv',
        'genre': 'genre.csv',
        'title_genre': 'genre_title.csv',
        'review': 'review.csv',
        'title': 'titles.csv',
    }
    access_files = {}
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    for model_name, files in files_dict.items():
        if files in files_list:
            print(f'Для модели {model_name} найден файл {files}')
            access_files[model_name] = files
        else:
            print(f'*Для модели {model_name} файл НЕ найден!')
    if len(files_dict) != len(access_files):
        raise TypeError('Найдены не все файлы!')
    return access_files


# def get_model_and_file(path, files, model_name):
#     models = {**apps.all_models['reviews'], **apps.all_models['users']}
#     if model_name in models:
#         model = models[model_name]
#     else:
#         raise TypeError('Такой модели не найдено')
#     if model_name in files:
#         file = files[model_name]
#         file_path = join(path, file)
#     else:
#         raise TypeError('Файл для этой модели не найден')
#     return model, file_path


def get_models_and_files(path, files):
    models = {**apps.all_models['reviews'], **apps.all_models['users']}
    models_files = {}
    for model_name, file_name in files.items():
        if model_name in models:
            model = models[model_name]
        else:
            raise TypeError('Такой модели не найдено')
        file_path = join(path, file_name)
        models_files[model_name] = (model, file_path)
    return models_files


def load_data(models_files):
    models_names_list = [
        'user',
        'category',
        'genre',
        'title',
        'review',
        'comment',
    ]
    for model_name in models_names_list:
        model, file = models_files[model_name]
        count_obj_before = model.objects.all().count()
        with open(file, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            print(f'Импорт данных в модель {model.__name__}')
            for row in reader:
                if 'author' in row.keys():
                    author = models_files['user'][0].objects.get(id=row['author'])
                    row['author'] = author
                object, created = model.objects.get_or_create(**row)
            count_row = reader.line_num - 1
        count_obj_after = model.objects.all().count()
        print(f'Добавлено {count_obj_after - count_obj_before} из {count_row}')


def load_users_data(path, files):
    model, file = get_model_and_file(path, files, 'user')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


def load_category_data(path, files):
    model, file = get_model_and_file(path, files, 'category')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


def load_genre_data(path, files):
    model, file = get_model_and_file(path, files, 'genre')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


def load_title_data(path, files):
    model, file = get_model_and_file(path, files, 'title')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            category = Category.objects.get(id=row['category'])
            row['category'] = category
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


def load_review_data(path, files):
    model, file = get_model_and_file(path, files, 'review')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            author = User.objects.get(id=row['author'])
            row['author'] = author
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


def load_comment_data(path, files):
    model, file = get_model_and_file(path, files, 'comment')
    count_before = model.objects.all().count()
    with open(file, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        print(f'Импорт данных в модель {model.__name__}')
        for row in reader:
            author = User.objects.get(id=row['author'])
            row['author'] = author
            object, created = model.objects.get_or_create(**row)
        count_row = reader.line_num - 1
    count_after = model.objects.all().count()
    print(f'Импортировано {count_after - count_before} из {count_row}')


# for key, value in row.items():
#     if value.isdigit():
#         row[key] = int(value)
# def load_data(files, path):
#     models = {**apps.all_models['reviews'], **apps.all_models['users']}
#     for model_name, file in files.items():
#         if model_name in models:
#             model = models[model_name]
#             print(f'Импорт в таблицу {model_name}')
#             print(model._meta.get_fields())
#             # print(model_name)
#             file_path = join(path, file)
#             with open(file_path, encoding='utf-8') as csv_file:
#                 reader = csv.DictReader(csv_file, delimiter=',')
#                 for count, row in enumerate(reader):
#                     print(row)
#                     for key, value in row.items():
#                         if value.isdigit():
#                             row[key] = int(value)
#                         # if key == 'author':
#                         #     author = User.objects.get(id=value)
#                         #     row[key] = author
#                     object, created = model.objects.get_or_create(**row)
#                 print(f'Импортированно {count} из {len(list(reader))}')    


#     # files_name_list = [splitext(name) for name in files_list]
