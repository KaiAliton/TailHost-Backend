from rest_framework import serializers
from ..abstract.serializers import AbstractSerializer
from .models import User


class UserSerializer(AbstractSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email',
                  'is_active', 'created', 'updated']
        read_only_field = ['is_active']
