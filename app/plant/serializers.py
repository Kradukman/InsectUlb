from rest_framework import serializers

from core.models import PlantFamilies, PlantGenera, PlantSpecies


class PlantFamiliesSerializer(serializers.ModelSerializer):
    """Serializer for plant families objects"""

    class Meta:
        model = PlantFamilies
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PlantGeneraSerializer(serializers.ModelSerializer):
    """Serializer for plant Genus objects"""
    family = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=PlantFamilies.objects.all()
                        )

    class Meta:
        model = PlantGenera
        fields = ('id', 'name', 'family')
        read_only_fields = ('id',)
        required_fields = ('name', 'family')


class PlantSpeciesSerializer(serializers.ModelSerializer):
    """Serializer for plant Specie objects"""
    genus = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=PlantGenera.objects.all()
                        )

    class Meta:
        model = PlantSpecies
        fields = ('id', 'name', 'genus')
        read_only_fields = ('id',)
