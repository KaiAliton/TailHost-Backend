
from ..abstract.serializers import AbstractSerializer
from .models import User
from ..genre.serializers import GenreSerializer


class UserSerializer(AbstractSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['genres'] = GenreSerializer(instance.genres, many=True).data
        return rep

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'cover',
                  'is_active', 'created', 'updated']
        read_only_field = ['is_active']
