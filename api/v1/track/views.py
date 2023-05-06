import datetime
import time

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.v1.abstract.views import AbstractViewSet
from api.v1.mixin.views import PaginatedResponseMixin
from apps.track.models import Track
from apps.track.serializers import TrackSerializer
from apps.auth.permissions import UserPermission
from rest_framework.response import Response
from django.core.paginator import Paginator


class TrackViewSet(PaginatedResponseMixin, AbstractViewSet):
    http_method_names = ('post', 'get', 'patch', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = TrackSerializer

    def get_queryset(self):
        if not self.request.user.is_anonymous and self.request.user.is_superuser:
            return Track.objects.all()
        return Track.objects.filter(approved=1)

    def get_object(self):
        obj = Track.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def popular(self, request, *args, **kwargs):
        tracks = Track.objects.filter(approved=1,
                                      created__gte=(datetime.datetime.now() - datetime.timedelta(days=30))).order_by(
            "?")
        page = self.paginate_queryset(tracks)
        if page is not None:
            serializer = TrackSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def queue(self, request, *args, **kwargs):
        tracks = Track.objects.filter(approved=1).order_by("?")
        return self.paginated_response(tracks, TrackSerializer, page_size=5)

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        track = self.get_object()
        user = self.request.user

        user.like_track(track)

        serializer = self.serializer_class(track)

        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        track = self.get_object()
        user = self.request.user

        user.remove_like_track(track)

        serializer = self.serializer_class(track)

        return Response(serializer.data)
