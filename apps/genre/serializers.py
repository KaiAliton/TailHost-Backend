from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.abstract.serializers import AbstractSerializer
from apps.genre.models import Genre
from apps.user.serializers import UserSerializer
from apps.comment.serializers import CommentSerializer
from apps.post.models import Post
from apps.user.models import User
from apps.comment.models import Comment


class GenreSerializer(AbstractSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']
