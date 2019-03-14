from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_plantFamily,
        sample_plantGene,
        sample_plantSpecie
    )

from plant import serializers


FAMILY_URL = reverse('plant:plantfamilies-list')
# workspace + viewset name + function

GENE_URL = reverse('plant:plantgenes-list')

SPECIE_URL = reverse('plant:plantspecies-list')


def detail_family_url(family_id):
    """Return the detail url for plant family"""
    return reverse('plant:plantfamilies-detail', args=[family_id])


def detail_gene_url(gene_id):
    """Return the detail url for plant gene"""
    return reverse('plant:plantgenes-detail', args=[gene_id])


def detail_specie_url(specie_id):
    """Return the detail url for plant specie"""
    return reverse('plant:plantspecies-detail', args=[specie_id])


class PublicPlantApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(FAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlantApiTests(TestCase):
    """Test private as user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_admin_required(self):
        """Test admin is required"""
        res = self.client.get(FAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePlantApiAsAdminTests(TestCase):
    """Test API as admin"""

    def setUp(self):
        self.user = create_superuser(
                        email='admin@ulb.ac.be',
                        password='test123'
                    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_families(self):
        """Test listing families"""
        sample_plantFamily()
        sample_plantFamily(name='test 2')

        res = self.client.get(FAMILY_URL)

        families = models.PlantFamilies.objects.all().order_by('id')
        serializer = serializers.PlantFamiliesSerializer(families, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_family(self):
        """Test retrieving a family"""
        family = sample_plantFamily()

        url = detail_family_url(family.id)
        res = self.client.get(url)

        serializer = serializers.PlantFamiliesSerializer(family)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_family(self):
        """Test creating a family"""
        payload = {'name': 'family test name'}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        family = models.PlantFamilies.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(family, key))

    def test_update_family(self):
        """Test updating family"""
        family = sample_plantFamily()
        payload = {'name': 'new family name'}

        url = detail_family_url(family.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        family.refresh_from_db()

        self.assertEqual(family.name, payload['name'])

    def test_list_genes(self):
        """Test listing genes"""
        sample_plantGene()
        sample_plantGene(name='test 2')

        res = self.client.get(GENE_URL)

        genes = models.PlantGenes.objects.all().order_by('id')
        serializer = serializers.PlantGenesSerializer(genes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_gene(self):
        """Test retrieving a gene"""
        gene = sample_plantGene()

        url = detail_gene_url(gene.id)
        res = self.client.get(url)

        serializer = serializers.PlantGenesSerializer(gene)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_gene(self):
        """Test creating a gene"""
        family = sample_plantFamily()
        payload = {'name': 'gene test name', 'family_id': family.id}

        res = self.client.post(GENE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        gene = models.PlantGenes.objects.get(id=res.data['id'])
        self.assertEqual(gene.name, payload['name'])
        self.assertEqual(gene.family.id, payload['family_id'])

    def test_update_gene(self):
        """Test updating gene²"""
        gene = sample_plantGene()
        family = sample_plantFamily(name='other family')
        payload = {'name': 'new gene name', 'family_id': family.id}

        url = detail_gene_url(gene.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        gene.refresh_from_db()

        self.assertEqual(gene.name, payload['name'])
        self.assertEqual(gene.family.id, payload['family_id'])

    def test_list_species(self):
        """Test listing species"""
        sample_plantSpecie()
        sample_plantSpecie(name='test 2')

        res = self.client.get(SPECIE_URL)

        species = models.PlantSpecies.objects.all().order_by('id')
        serializer = serializers.PlantSpeciesSerializer(species, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_specie(self):
        """Test retrieving a specie"""
        specie = sample_plantSpecie()

        url = detail_specie_url(specie.id)
        res = self.client.get(url)

        serializer = serializers.PlantSpeciesSerializer(specie)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_specie(self):
        """Test creating a specie"""
        gene = sample_plantGene()
        payload = {'name': 'specie test name', 'gene_id': gene.id}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        specie = models.PlantSpecies.objects.get(id=res.data['id'])
        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.gene.id, payload['gene_id'])

    def test_update_specie(self):
        """Test updating specie²"""
        specie = sample_plantSpecie()
        gene = sample_plantGene(name='other gene')
        payload = {'name': 'new specie name', 'gene_id': gene.id}

        url = detail_specie_url(specie.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        specie.refresh_from_db()

        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.gene.id, payload['gene_id'])
