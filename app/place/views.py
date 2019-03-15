from core.views import BasePermissionsViewset

from core.models import (
                    PlaceType,
                    Country,
                    Region,
                    City,
                    Town
                )

from place import serializers


class PlaceTypeViewset(BasePermissionsViewset):
    """Manage place type"""
    serializer_class = serializers.PlaceTypeSerializer
    queryset = PlaceType.objects.all()


class CountryViewset(BasePermissionsViewset):
    """Manage country"""
    serializer_class = serializers.CountrySerializer
    queryset = Country.objects.all()


class RegionViewset(BasePermissionsViewset):
    """Manage region"""
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()


class CityViewset(BasePermissionsViewset):
    """Manage city"""
    serializer_class = serializers.CitySerializer
    queryset = City.objects.all()


class TownViewset(BasePermissionsViewset):
    """Manage Town"""
    serializer_class = serializers.TownSerializer
    queryset = Town.objects.all()
