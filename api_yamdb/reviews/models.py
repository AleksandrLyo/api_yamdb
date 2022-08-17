from django.db import models


class Categories(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.name
