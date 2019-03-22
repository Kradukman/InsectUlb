from core.views import BasePermissionsViewset
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions


from core.models import (
                    PlaceType,
                    Country,
                    Region,
                    City,
                    Town,
                    Place
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


class PlaceViewset(BasePermissionsViewset):
    """Manage Place"""
    serializer_class = serializers.PlaceSerializer
    queryset = Place.objects.all()

    @action(
        methods=['patch'],
        detail=True,
        url_path='add-project',
        url_name='add_project'
    )
    def add_project(self, request, pk=None):
        response = {}
        # get serializer
        serializer = self.get_serializer()
        place = serializer.add_project(
                place_id=pk,
                project_id=self.request.data['project']
            )
        placeSerializer = serializers.PlaceDetailSerializer(place)
        response['data'] = placeSerializer.data
        return Response(response)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action in ['retrieve', 'add_project', ]:
            return serializers.PlaceDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve', ]:
            self.permission_classes = [permissions.IsAuthenticated, ]
        if self.action in [
            'create',
            'update',
            'partial_update',
            'add_project'
        ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        return [permission() for permission in self.permission_classes]
