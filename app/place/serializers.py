from rest_framework import serializers

from core.models import (
                    PlaceType,
                    Country
                )


class PlaceTypeSerializer(serializers.ModelSerializer):
    """Serializer for PlaceType objects"""

    class Meta:
        model = PlaceType
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country objects"""

    class Meta:
        model = Country
        fields = ('id', 'name')
        read_only_fields = ('id',)
