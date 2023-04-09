from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


class GenreManager(AbstractManager):
    pass


class Genre(AbstractModel):
    title = models.TextField()
    objects = GenreManager()

    def __str__(self):
        return f'{self.title}'
