from django.contrib import admin

from apps.track.models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'album', 'genre')
# Register your models here.
