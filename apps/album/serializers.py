from apps.album.models import Album
from apps.user.models import User
from apps.abstract.serializers import AbstractSerializer
from apps.user.serializers import UserSerializer
from apps.user.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class AlbumSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id')
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous:
            return False
        return request.user.has_liked_track(instance)

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't change author of track.")
        return value

    class Meta:
        model = Album
        fields = ['id', 'author', 'title', 'cover', 'created', 'updated'
                                                               'cover', 'liked', 'likes_count']
