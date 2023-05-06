from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlencode

base_url = "/media/"
UserProfile = get_user_model()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(base_url + obj.avatar.name))

    def genres_tag(self, obj):
        return ','.join([x.title for x in obj.genres.all()])

    def cover_tag(self, obj):
        return format_html(
            '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(base_url + obj.cover.name))

    search_fields = ['username']
    list_display = ('username', 'image_tag', 'cover_tag', 'genres_tag')
    list_filter = ('genres',)

# Register your models here.
