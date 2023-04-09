import datetime

from django.core.paginator import Paginator
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.abstract.views import AbstractViewSet
from apps.genre.models import Genre
from rest_framework.response import Response

from apps.genre.serializers import GenreSerializer
from apps.track.models import Track
from apps.track.serializers import TrackSerializer


class GenreViewSet(AbstractViewSet):
    http_method_names = ('get')
    permission_classes = (AllowAny,)
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()

    def get_object(self):
        obj = Genre.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(methods=['get'], detail=True)
    def get_popular(self, request, *args, **kwargs):
        genre = self.get_object()
        tracks = Track.objects.filter(genre=genre, created__gte=(datetime.datetime.now() - datetime.timedelta(days=7)))[
                 :10]
        genre_serializer = GenreSerializer(genre)
        track_serizalizer = TrackSerializer(tracks, many=True)
        output = [
            {"genre": genre_serializer.data},
            {"tracks": track_serizalizer.data},
        ]
        return Response(output)

    @action(methods=['get'], detail=True)
    def tracks(self, request, *args, **kwargs):
        genre = self.get_object()
        tracks = Track.objects.get_objects_by_genre(genre=genre)
        paginate = self.paginate_queryset(tracks)
        genre_serializer = GenreSerializer(genre)
        track_serializer = TrackSerializer(paginate, many=True)
        output = [
            {"genre": genre_serializer.data},
            {"tracks": track_serializer.data},
        ]
        return Response(output)
