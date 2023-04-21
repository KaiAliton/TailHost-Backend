from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


# Create your models here.

class AlbumManager(AbstractManager):
    pass


class Album(AbstractModel):
    author = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    title = models.TextField()
    cover = models.ImageField(upload_to='covers/')
    objects = AlbumManager()

    def __str__(self):
        return f'{self.author.name}'
