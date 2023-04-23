from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.v1.abstract.views import AbstractViewSet
from apps.post.models import Post
from apps.post.serializers import PostSerializer
from apps.auth.permissions import UserPermission
from rest_framework.response import Response


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'patch', 'delete')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.like_post(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        user.remove_like_post(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data)
