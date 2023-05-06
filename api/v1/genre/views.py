import datetime

from django.core.paginator import Paginator
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.abstract.views import AbstractViewSet
from api.v1.mixin.views import PaginatedResponseMixin
from apps.genre.models import Genre
from rest_framework.response import Response

from apps.genre.serializers import GenreSerializer
from apps.track.models import Track
from apps.track.serializers import TrackSerializer
from apps.user.models import User
from apps.user.serializers import UserSerializer


class GenreViewSet(PaginatedResponseMixin, AbstractViewSet):
    http_method_names = ('get')
    permission_classes = (AllowAny,)
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()

    def get_object(self):
        obj = Genre.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(methods=['get'], detail=True)
    def popular(self, request, *args, **kwargs):
        genre = self.get_object()
        tracks = Track.objects.filter(genre=genre, created__gte=(datetime.datetime.now() - datetime.timedelta(days=7)))[
                 :12]
        genre_serializer = GenreSerializer(genre)
        track_serizalizer = TrackSerializer(tracks, many=True)
        output = {
            "genre": genre_serializer.data,
            "tracks": track_serizalizer.data,
        }
        return Response(output)

    @action(methods=['get'], detail=True)
    def overview(self, request, *args, **kwargs):
        genre = self.get_object()
        genre_serializer = GenreSerializer(genre)
        tracks = Track.objects.filter(genre=genre)[
                 :12]
        users = User.objects.filter(genres=genre)[:12]
        track_serializer = TrackSerializer(tracks, many=True)
        user_serializer = UserSerializer(users, many=True)
        output = {
            "genre": genre_serializer.data,
            "users": user_serializer.data,
            "tracks": track_serializer.data
        }
        return Response(output)

    @action(methods=['get'], detail=True)
    def tracks(self, request, *args, **kwargs):
        genre = self.get_object()
        genre_serializer = GenreSerializer(genre)
        tracks = Track.objects.get_objects_by_genre(genre=genre)
        page = self.paginate_queryset(tracks)
        if page is not None:
            serializer = TrackSerializer(page, many=True)
            output = {
                "genre": genre_serializer.data,
                "tracks": serializer.data
            }
            return self.get_paginated_response(output)
        serializer = TrackSerializer(tracks, many=True)
        output = {
            "genre": genre_serializer.data,
            "tracks": serializer.data
        }
        return Response(output)
