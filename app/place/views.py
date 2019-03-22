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

    @action(
        methods=['patch'],
        detail=True,
        url_path='remove-project',
        url_name='remove_project'
    )
    def remove_project(self, request, pk=None):
        response = {}
        # get serializer
        serializer = self.get_serializer()
        place = serializer.remove_project(
                place_id=pk,
                project_id=self.request.data['project']
            )
        placeSerializer = serializers.PlaceDetailSerializer(place)
        response['data'] = placeSerializer.data
        return Response(response)

    @action(
        methods=['patch'],
        detail=True,
        url_path='update-attribute',
        url_name='update_attribute'
    )
    def update_attribute(self, request, pk=None):
        """Update foreignkey and many to many fields"""
        response = {}
        old_project_id = None
        new_project_id = None
        town_id = None
        type_id = None
        if 'old_project_id' in self.request.data:
            if self.request.data['old_project_id'] is not None:
                old_project_id = self.request.data['old_project_id']
        if 'new_project_id' in self.request.data:
            if self.request.data['new_project_id'] is not None:
                new_project_id = self.request.data['new_project_id']
        if 'town_id' in self.request.data:
            if self.request.data['town_id'] is not None:
                town_id = self.request.data['town_id']
        if 'type_id' in self.request.data:
            if self.request.data['type_id'] is not None:
                type_id = self.request.data['type_id']
        # get serializer
        serializer = self.get_serializer()
        place = serializer.update_attribute(
                place_id=pk,
                old_project_id=old_project_id,
                project_id=new_project_id,
                type_id=type_id,
                town_id=town_id
            )
        placeSerializer = serializers.PlaceDetailSerializer(place)
        response['data'] = placeSerializer.data
        return Response(response)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action in [
            'retrieve',
            'add_project',
            'update_attribute',
            'remove_project'
        ]:
            return serializers.PlaceDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve', ]:
            self.permission_classes = [permissions.IsAuthenticated, ]
        if self.action in [
            'create',
            'update',
            'partial_update',
            'add_project',
            'remove_project',
            'update_attribute'
        ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        return [permission() for permission in self.permission_classes]
