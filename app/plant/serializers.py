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

    class Meta:
        model = PlantGenes
        fields = ('id', 'name', 'family_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create gene"""
        family = PlantFamilies.objects.get(
                    id=self.context['request'].data['family_id']
                )
        return PlantGenes.objects.create(
                    name=validated_data['name'],
                    family=family
                )

    def update(self, instance, validated_data):
        """Partial_update gene"""
        gene = PlantGenes.objects.get(id=self.data['id'])
        if self.context['request'].data['family_id']:
            family = PlantFamilies.objects.get(
                        id=self.context['request'].data['family_id']
                    )
            gene.family = family
            gene.save()
        gene = super().update(gene, validated_data)

        return gene


class PlantSpeciesSerializer(serializers.ModelSerializer):
    """Serializer for plant Specie objects"""

    class Meta:
        model = PlantSpecies
        fields = ('id', 'name', 'gene_id')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create specie"""
        gene = PlantGenes.objects.get(
                    id=self.context['request'].data['gene_id']
                )
        return PlantSpecies.objects.create(
                    name=validated_data['name'],
                    gene=gene
                )

    def update(self, instance, validated_data):
        """Partial_update specie"""
        specie = PlantSpecies.objects.get(id=self.data['id'])
        if self.context['request'].data['gene_id']:
            gene = PlantGenes.objects.get(
                        id=self.context['request'].data['gene_id']
                    )
            specie.gene = gene
            specie.save()
        specie = super().update(specie, validated_data)

        return specie
