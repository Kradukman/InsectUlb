from rest_framework import viewsets, authentication, permissions

from core.models import PlantFamilies, PlantGenes, PlantSpecies

from plant import serializers


class BasePlantViewset(viewsets.ModelViewSet):
    """Base viewset to manage plants as admin"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )


class PlantFamiliesViewset(BasePlantViewset):
    """Manage plant families as admin"""
    serializer_class = serializers.PlantFamiliesSerializer
    queryset = PlantFamilies.objects.all()


class PlantGenesViewset(BasePlantViewset):
    """Manage plant Genes as admin"""
    serializer_class = serializers.PlantGenesSerializer
    queryset = PlantGenes.objects.all()


class PlantSpeciesViewset(BasePlantViewset):
    """Manage plant species as admin"""
    serializer_class = serializers.PlantSpeciesSerializer
    queryset = PlantSpecies.objects.all()
