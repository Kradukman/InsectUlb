from core.views import BasePermissionsViewset

from core.models import (
                    InsectSuperFamilies,
                    InsectFamilies,
                    InsectSubFamilies,
                    InsectTribes,
                    InsectGenera,
                    InsectSpecies,
                    InsectGodfather,
                    InsectTrap
                )

from insect import serializers


class InsectSuperFamiliesViewset(BasePermissionsViewset):
    """Manage insect super families as admin"""
    serializer_class = serializers.InsectSuperFamiliesSerializer
    queryset = InsectSuperFamilies.objects.all()


class InsectFamiliesViewset(BasePermissionsViewset):
    """Manage insect families as admin"""
    serializer_class = serializers.InsectFamiliesSerializer
    queryset = InsectFamilies.objects.all()


class InsectSubFamiliesViewset(BasePermissionsViewset):
    """Manage insect sub families as admin"""
    serializer_class = serializers.InsectSubFamiliesSerializer
    queryset = InsectSubFamilies.objects.all()


class InsectTribesViewset(BasePermissionsViewset):
    """Manage insect tribes as admin"""
    serializer_class = serializers.InsectTribesSerializer
    queryset = InsectTribes.objects.all()


class InsectGeneraViewset(BasePermissionsViewset):
    """Manage insect Genera as admin"""
    serializer_class = serializers.InsectGeneraSerializer
    queryset = InsectGenera.objects.all()


class InsectGodfatherViewset(BasePermissionsViewset):
    """Manage insect godfather as admin"""
    serializer_class = serializers.InsectGodfatherSerializer
    queryset = InsectGodfather.objects.all()


class InsectTrapViewset(BasePermissionsViewset):
    """Manage insect trap as admin"""
    serializer_class = serializers.InsectTrapSerializer
    queryset = InsectTrap.objects.all()


class InsectSpeciesViewset(BasePermissionsViewset):
    """Manage insect Species as admin"""
    serializer_class = serializers.InsectSpeciesSerializer
    queryset = InsectSpecies.objects.all()
