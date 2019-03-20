from rest_framework import serializers

from core.models import (
                    PlaceType,
                    Country,
                    Region,
                    City,
                    Town
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


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for plant Region objects"""
    country = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=Country.objects.all()
                        )

    class Meta:
        model = Region
        fields = ('id', 'name', 'country')
        read_only_fields = ('id',)
        required_fields = ('name', 'country')


class CitySerializer(serializers.ModelSerializer):
    """Serializer for plant City objects"""
    region = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=Region.objects.all()
                        )

    class Meta:
        model = City
        fields = ('id', 'name', 'region')
        read_only_fields = ('id',)
        required_fields = ('name', 'region')


class TownSerializer(serializers.ModelSerializer):
    """Serializer for plant Town objects"""
    city = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=City.objects.all()
                        )

    class Meta:
        model = Town
        fields = ('id', 'name', 'city')
        read_only_fields = ('id',)
        required_fields = ('name', 'city')
