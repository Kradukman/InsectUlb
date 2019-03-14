from core.views import BasePermissionsViewset

from core.models import (
                    PlaceType,
                    Country
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
