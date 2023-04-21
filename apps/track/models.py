from django.db import models
from ..abstract.models import AbstractModel, AbstractManager
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# Create your models here.

class TrackManager(AbstractManager):
    def get_objects_by_genre(self, genre):
        try:
            result = self.filter(genre=genre)
            return result
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404


class Track(AbstractModel):
    author = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    title = models.TextField()
    genre = models.ForeignKey(to='genre.Genre', on_delete=models.CASCADE, default=2, null=True)
    cover = models.ImageField(upload_to='covers/')
    approved = models.BooleanField(default=0)
    album = models.ForeignKey(to='album.Album', on_delete=models.CASCADE, related_name='tracks')
    music = models.FileField(upload_to='music/')
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    edited = models.BooleanField(default=False)
    objects = TrackManager()

    def __str__(self):
        return f'{self.author.name}'
