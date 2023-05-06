from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.album.models import Album
from apps.album.serializers import AlbumSerializer
from apps.genre.models import Genre
from apps.genre.serializers import GenreSerializer
from apps.user.serializers import UserSerializer
from apps.track.models import Track
from apps.user.models import User


class TrackSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id')
    album = serializers.SlugRelatedField(
        queryset=Album.objects.all(), slug_field='public_id')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='public_id')
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
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if self.context:
            if not self.context['request'].user.is_anonymous and self.context["request"].user.is_superuser:
                rep['approved'] = instance.approved
        author = User.objects.get_object_by_public_id(rep["author"])
        album = Album.objects.get_object_by_public_id(rep['album'])
        genre = Genre.objects.get_object_by_public_id(rep["genre"])
        rep["genre"] = GenreSerializer(genre).data
        rep["author"] = UserSerializer(author).data
        rep["album"] = AlbumSerializer(album).data
        return rep

    def validate_album(self, value):
        if self.context['request'].user != value.author:
            raise ValidationError("check")
        else:
            raise ValidationError("good")

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't change author of track.")

        return value

    class Meta:
        model = Track
        fields = ['id', 'author', 'title', 'album', 'genre',
                  'created', 'liked', 'cover', 'likes_count', 'music', 'video']
        read_only_fields = ["edited"]
