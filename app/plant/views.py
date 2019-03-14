from core.views import BasePermissionsViewset

from core.models import PlantFamilies, PlantGenes, PlantSpecies

from plant import serializers


class PlantFamiliesViewset(BasePermissionsViewset):
    """Manage plant families as admin"""
    serializer_class = serializers.PlantFamiliesSerializer
    queryset = PlantFamilies.objects.all()


class PlantGenesViewset(BasePermissionsViewset):
    """Manage plant Genes as admin"""
    serializer_class = serializers.PlantGenesSerializer
    queryset = PlantGenes.objects.all()


class PlantSpeciesViewset(BasePermissionsViewset):
    """Manage plant species as admin"""
    serializer_class = serializers.PlantSpeciesSerializer
    queryset = PlantSpecies.objects.all()
