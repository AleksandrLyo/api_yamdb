# Generated by Django 2.2.16 on 2022-08-23 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'администратор'), ('moderator', 'модератор'), ('user', 'пользователь')], default='user', max_length=20),
        ),
    ]