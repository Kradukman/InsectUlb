from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_plantFamily,
        sample_plantGenus,
        sample_plantSpecie
    )

from plant import serializers


FAMILY_URL = reverse('plant:plantfamilies-list')
# workspace + viewset name + function

GENUS_URL = reverse('plant:plantgenera-list')

SPECIE_URL = reverse('plant:plantspecies-list')


def detail_family_url(family_id):
    """Return the detail url for plant family"""
    return reverse('plant:plantfamilies-detail', args=[family_id])


def detail_genus_url(genus_id):
    """Return the detail url for plant genus"""
    return reverse('plant:plantgenera-detail', args=[genus_id])


def detail_specie_url(specie_id):
    """Return the detail url for plant specie"""
    return reverse('plant:plantspecies-detail', args=[specie_id])


class PublicPlantApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_family_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(FAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genus_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(GENUS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_specie_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(SPECIE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlantApiTests(TestCase):
    """Test private as user"""

    def setUp(self):
        self.user = sample_user()
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

    def test_family_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'family test name'}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_genus_admin_required(self):
        """Test admin is required"""
        family = sample_plantFamily()
        payload = {'name': 'genus test name', 'family': family.id}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_specie_admin_required(self):
        """Test admin is required"""
        genus = sample_plantGenus()
        payload = {'name': 'specie test name', 'genus': genus.id}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_genera(self):
        """Test listing genera"""
        sample_plantGenus()
        sample_plantGenus(name='test 2')

        res = self.client.get(GENUS_URL)

        genera = models.PlantGenera.objects.all().order_by('id')
        serializer = serializers.PlantGeneraSerializer(genera, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_genus(self):
        """Test retrieving a genus"""
        genus = sample_plantGenus()

        url = detail_genus_url(genus.id)
        res = self.client.get(url)

        serializer = serializers.PlantGeneraSerializer(genus)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

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


class PrivatePlantApiAsAdminTests(TestCase):
    """Test API as admin"""

    def setUp(self):
        self.user = create_superuser(
                        email='admin@ulb.ac.be',
                        password='test123'
                    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_family(self):
        """Test creating a family"""
        payload = {'name': 'family test name'}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        family = models.PlantFamilies.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(family, key))

    def test_create_family_no_name_fail(self):
        """Test creating a family without name should fail"""
        payload = {'name': ''}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_family(self):
        """Test updating family"""
        family = sample_plantFamily()
        payload = {'name': 'new family name'}

        url = detail_family_url(family.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        family.refresh_from_db()

        self.assertEqual(family.name, payload['name'])

    def test_create_genus(self):
        """Test creating a genus"""
        family = sample_plantFamily()
        payload = {'name': 'genus test name', 'family': family.id}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        genus = models.PlantGenera.objects.get(id=res.data['id'])
        self.assertEqual(genus.name, payload['name'])
        self.assertEqual(genus.family.id, payload['family'])

    def test_create_genus_no_name_fail(self):
        """Test creating a genus without name should fail"""
        payload = {'name': ''}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_genus(self):
        """Test updating genus"""
        genus = sample_plantGenus()
        family = sample_plantFamily(name='other family')
        payload = {'name': 'new gene name', 'family': family.id}

        url = detail_genus_url(genus.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        genus.refresh_from_db()

        self.assertEqual(genus.name, payload['name'])
        self.assertEqual(genus.family.id, payload['family'])

    def test_create_specie(self):
        """Test creating a specie"""
        genus = sample_plantGenus()
        payload = {'name': 'specie test name', 'genus': genus.id}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        specie = models.PlantSpecies.objects.get(id=res.data['id'])
        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.genus.id, payload['genus'])

    def test_create_specie_no_name_fail(self):
        """Test creating a specie without name should fail"""
        payload = {'name': ''}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_specie(self):
        """Test updating specie"""
        specie = sample_plantSpecie()
        genus = sample_plantGenus(name='other gene')
        payload = {'name': 'new specie name', 'genus': genus.id}

        url = detail_specie_url(specie.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        specie.refresh_from_db()

        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.genus.id, payload['genus'])
