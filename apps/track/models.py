from django.db import models
from ..abstract.models import AbstractModel, AbstractManager


# Create your models here.

class TrackManager(AbstractManager):
    pass


class Track(AbstractModel):
    author = models.ForeignKey(to='user.User', on_delete=models.CASCADE)
    title = models.TextField()
    cover = models.ImageField(upload_to='media/covers/')
    approved = models.BooleanField(default=0)
    music = models.FileField(upload_to='media/music/')
    video = models.FileField(upload_to='media/videos/', null=True, blank=True)
    edited = models.BooleanField(default=False)
    objects = TrackManager()

    def __str__(self):
        return f'{self.author.name}'
