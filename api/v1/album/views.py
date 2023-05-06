import datetime
import time

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.abstract.views import AbstractViewSet
from apps.album.models import Album
from apps.album.serializers import AlbumSerializer
from apps.track.models import Track
from apps.track.serializers import TrackSerializer
from apps.auth.permissions import UserPermission
from rest_framework.response import Response


class AlbumViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'patch', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.all()

    def get_object(self):
        obj = Album.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tracks(self, request, *args, **kwargs):
        album = self.get_object()
        album_serializer = AlbumSerializer(album)
        tracks = album.tracks.all()
        track_serializer = TrackSerializer(tracks, many=True)
        output = {
            "album": album_serializer.data,
            "tracks": track_serializer.data
        }
        return Response(output)
