from rest_framework import serializers

from core.models import PlantFamilies, PlantGenes, PlantSpecies


class PlantFamiliesSerializer(serializers.ModelSerializer):
    """Serializer for plant families objects"""

    class Meta:
        model = PlantFamilies
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PlantGenesSerializer(serializers.ModelSerializer):
    """Serializer for plant Gene objects"""
    family = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=PlantFamilies.objects.all()
                        )

    class Meta:
        model = PlantGenes
        fields = ('id', 'name', 'family')
        read_only_fields = ('id',)
        required_fields = ('name', 'family')


class PlantSpeciesSerializer(serializers.ModelSerializer):
    """Serializer for plant Specie objects"""
    gene = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=PlantGenes.objects.all()
                        )

    class Meta:
        model = PlantSpecies
        fields = ('id', 'name', 'gene')
        read_only_fields = ('id',)
