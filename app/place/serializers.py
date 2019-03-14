from rest_framework import serializers

from core.models import PlaceType


class PlaceTypeSerializer(serializers.ModelSerializer):
    """Serializer for plant PlaceType objects"""

    class Meta:
        model = PlaceType
        fields = ('id', 'name')
        read_only_fields = ('id',)
