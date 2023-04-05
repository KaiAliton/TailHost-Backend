from django.contrib import admin
from django import forms

from django.contrib.auth import get_user_model

UserProfile = get_user_model()
admin.site.register(UserProfile)

# Register your models here.
