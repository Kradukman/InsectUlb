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

    class Meta:
        model = Region
        fields = ('id', 'name', 'country_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create gene"""
        country = Country.objects.get(
                    id=self.context['request'].data['country_id']
                )
        return Region.objects.create(
                    name=validated_data['name'],
                    country=country
                )

    def update(self, instance, validated_data):
        """Partial_update Region"""
        region = Region.objects.get(id=self.data['id'])
        if self.context['request'].data['country_id']:
            country = Country.objects.get(
                        id=self.context['request'].data['country_id']
                    )
            region.country = country
            region.save()
        region = super().update(region, validated_data)

        return region


class CitySerializer(serializers.ModelSerializer):
    """Serializer for plant City objects"""

    class Meta:
        model = City
        fields = ('id', 'name', 'region_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create gene"""
        region = Region.objects.get(
                    id=self.context['request'].data['region_id']
                )
        return City.objects.create(
                    name=validated_data['name'],
                    region=region
                )

    def update(self, instance, validated_data):
        """Partial_update City"""
        city = City.objects.get(id=self.data['id'])
        if self.context['request'].data['region_id']:
            region = Region.objects.get(
                        id=self.context['request'].data['region_id']
                    )
            city.region = region
            city.save()
        city = super().update(city, validated_data)

        return city


class TownSerializer(serializers.ModelSerializer):
    """Serializer for plant Town objects"""

    class Meta:
        model = Town
        fields = ('id', 'name', 'city_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create gene"""
        city = City.objects.get(
                    id=self.context['request'].data['city_id']
                )
        return Town.objects.create(
                    name=validated_data['name'],
                    city=city
                )

    def update(self, instance, validated_data):
        """Partial_update Town"""
        town = Town.objects.get(id=self.data['id'])
        if self.context['request'].data['city_id']:
            city = City.objects.get(
                        id=self.context['request'].data['city_id']
                    )
            town.city = city
            town.save()
        town = super().update(town, validated_data)

        return town
