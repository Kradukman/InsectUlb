from rest_framework import serializers

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


class InsectSuperFamiliesSerializer(serializers.ModelSerializer):
    """Serializer for insect super families objects"""

    class Meta:
        model = InsectSuperFamilies
        fields = ('id', 'name')
        read_only_fields = ('id',)


class InsectFamiliesSerializer(serializers.ModelSerializer):
    """Serializer for insect families objects"""
    superFamily = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectSuperFamilies.objects.all()
                        )

    class Meta:
        model = InsectFamilies
        fields = ('id', 'name', 'superFamily')
        read_only_fields = ('id',)
        required_fields = ('name', 'superFamily')


class InsectSubFamiliesSerializer(serializers.ModelSerializer):
    """Serializer for insect sub families objects"""
    family = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectFamilies.objects.all()
                        )

    class Meta:
        model = InsectSubFamilies
        fields = ('id', 'name', 'family')
        read_only_fields = ('id',)
        required_fields = ('name', 'family')


class InsectTribesSerializer(serializers.ModelSerializer):
    """Serializer for insect tribes objects"""
    subFamily = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectSubFamilies.objects.all()
                        )

    class Meta:
        model = InsectTribes
        fields = ('id', 'name', 'subFamily')
        read_only_fields = ('id',)
        required_fields = ('name', 'subFamily')


class InsectGeneraSerializer(serializers.ModelSerializer):
    """Serializer for insect genera objects"""
    tribe = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectTribes.objects.all()
                        )

    class Meta:
        model = InsectGenera
        fields = ('id', 'name', 'tribe')
        read_only_fields = ('id',)
        required_fields = ('name', 'tribe')


class InsectGodfatherSerializer(serializers.ModelSerializer):
    """Serializer for insect godfather objects"""
    class Meta:
        model = InsectGodfather
        fields = ('id', 'name')
        read_only_fields = ('id',)
        required_fields = ('name')


class InsectTrapSerializer(serializers.ModelSerializer):
    """Serializer for insect trap objects"""
    class Meta:
        model = InsectTrap
        fields = ('id', 'name')
        read_only_fields = ('id',)
        required_fields = ('name')


class InsectSpeciesSerializer(serializers.ModelSerializer):
    """Serializer for insect species objects"""
    genus = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectGenera.objects.all()
                        )
    godfather = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=InsectGodfather.objects.all()
                        )

    class Meta:
        model = InsectSpecies
        fields = ('id', 'name', 'genus', 'godfather', 'year', 'otherName')
        read_only_fields = ('id',)
        required_fields = ('name', 'genus')
