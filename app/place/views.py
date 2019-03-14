from core.views import BasePermissionsViewset

from core.models import PlaceType

from place import serializers


class PlaceTypeViewset(BasePermissionsViewset):
    """Manage place type"""
    serializer_class = serializers.PlaceTypeSerializer
    queryset = PlaceType.objects.all()
