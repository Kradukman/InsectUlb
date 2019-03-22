from rest_framework import serializers
from project.serializers import ProjectSerializer

from core.models import (
                    PlaceType,
                    Country,
                    Region,
                    City,
                    Town,
                    Place,
                    Project
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
    """Serializer for Town objects"""
    city = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=City.objects.all()
                        )

    class Meta:
        model = Town
        fields = ('id', 'name', 'city')
        read_only_fields = ('id',)
        required_fields = ('name', 'city')


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for place objects"""
    projects = serializers.PrimaryKeyRelatedField(
                            many=True, queryset=Project.objects.all()
                        )
    type = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=PlaceType.objects.all()
                        )
    town = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=Town.objects.all()
                        )

    class Meta:
        model = Place
        fields = (
                'id',
                'name',
                'type',
                'town',
                'codeSite',
                'projects',
                'comment',
                'latitudeLambert72',
                'longitudeLambert72',
                'latitudeDec',
                'longitudeDec'
            )
        read_only_fields = ('id',)
        # required_fields = (
        #         'name',
        #         'type',
        #         'codeSite',
        #         'town',
        #         'latitudeDec',
        #         'longitudeDec'
        #     )


class PlaceDetailSerializer(PlaceSerializer):
    """Serialize a place detail"""
    projects = ProjectSerializer(many=True)
    town = TownSerializer(many=False)
    type = PlaceTypeSerializer(many=False)

    def create(self, validated_data):
        pass

    def add_project(self, place_id, project_id):
        project = Project.objects.get(id=project_id)
        place = Place.objects.get(id=place_id)
        place.projects.add(project)
        place.save()
        return place
