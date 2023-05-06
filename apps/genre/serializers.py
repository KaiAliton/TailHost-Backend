
from apps.abstract.serializers import AbstractSerializer
from apps.genre.models import Genre


class GenreSerializer(AbstractSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title']
