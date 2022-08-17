from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        null=True,
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
