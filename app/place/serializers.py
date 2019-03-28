from rest_framework import serializers

from core.models import (
                    PlaceType,
                    Country,
                    Region,
                    City,
                    Town,
                    Place,
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
                'comment',
                'latitudeLambert72',
                'longitudeLambert72',
                'latitudeDec',
                'longitudeDec'
            )
        read_only_fields = ('id',)


class PlaceDetailSerializer(PlaceSerializer):
    """Serialize a place detail"""
    # projects = ProjectSerializer(many=True)
    town = TownSerializer(many=False)
    type = PlaceTypeSerializer(many=False)

    def create(self, validated_data):
        pass

    # def add_project(self, place_id, project_id):
    #     project = Project.objects.get(id=project_id)
    #     place = Place.objects.get(id=place_id)
    #     place.projects.add(project)
    #     place.save()
    #     return place
    #
    # def remove_project(self, place_id, project_id):
    #     project = Project.objects.get(id=project_id)
    #     place = Place.objects.get(id=place_id)
    #     place.projects.remove(project)
    #     place.save()
    #     return place

    def update_attribute(
        self,
        place_id,
        town_id=None,
        type_id=None
    ):
        place = Place.objects.get(id=place_id)
        # if project_id and old_project_id is not None:
        #     project = Project.objects.get(id=old_project_id)
        #     place.projects.remove(project)
        #     project = Project.objects.get(id=project_id)
        #     place.projects.add(project)
        if type_id is not None:
            type = PlaceType.objects.get(id=type_id)
            place.type = type
            place.save()
        if town_id is not None:
            town = Town.objects.get(id=town_id)
            place.town = town
            place.save()

        return place
