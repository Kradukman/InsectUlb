from core.views import BasePermissionsViewset

from core.models import PlantFamilies, PlantGenera, PlantSpecies

from plant import serializers


class PlantFamiliesViewset(BasePermissionsViewset):
    """Manage plant families as admin"""
    serializer_class = serializers.PlantFamiliesSerializer
    queryset = PlantFamilies.objects.all()


class PlantGeneraViewset(BasePermissionsViewset):
    """Manage plant Genes as admin"""
    serializer_class = serializers.PlantGeneraSerializer
    queryset = PlantGenera.objects.all()


class PlantSpeciesViewset(BasePermissionsViewset):
    """Manage plant species as admin"""
    serializer_class = serializers.PlantSpeciesSerializer
    queryset = PlantSpecies.objects.all()
