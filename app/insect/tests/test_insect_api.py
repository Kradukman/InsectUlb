from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_insectSuperFamily,
        sample_insectFamily,
        sample_insectSubFamily,
        sample_insectTribe,
        sample_insectGenus,
        sample_insectSpecie,
        sample_insectGodfather,
        sample_insectTrap
    )

from insect import serializers

SUPERFAMILY_URL = reverse('insect:insectsuperfamilies-list')
# workspace + viewset name + function

FAMILY_URL = reverse('insect:insectfamilies-list')

SUBFAMILY_URL = reverse('insect:insectsubfamilies-list')

TRIBE_URL = reverse('insect:insecttribes-list')

GENUS_URL = reverse('insect:insectgenera-list')

SPECIE_URL = reverse('insect:insectspecies-list')

GODFATHER_URL = reverse('insect:insectgodfather-list')

TRAP_URL = reverse('insect:insecttrap-list')


def detail_super_family_url(supFamily_id):
    """Return the detail url for insect super family"""
    return reverse('insect:insectsuperfamilies-detail', args=[supFamily_id])


def detail_family_url(family_id):
    """Return the detail url for insect family"""
    return reverse('insect:insectfamilies-detail', args=[family_id])


def detail_sub_family_url(subfamily_id):
    """Return the detail url for insect sub family"""
    return reverse('insect:insectsubfamilies-detail', args=[subfamily_id])


def detail_tribe_url(tribe_id):
    """Return the detail url for insect tribe"""
    return reverse('insect:insecttribes-detail', args=[tribe_id])


def detail_genus_url(genus_id):
    """Return the detail url for insect genus"""
    return reverse('insect:insectgenera-detail', args=[genus_id])


def detail_specie_url(specie_id):
    """Return the detail url for insect specie"""
    return reverse('insect:insectspecies-detail', args=[specie_id])


def detail_godfather_url(godfather_id):
    """Return the detail url for insect godfather"""
    return reverse('insect:insectgodfather-detail', args=[godfather_id])


def detail_trap_url(trap_id):
    """Return the detail url for trap"""
    return reverse('insect:insecttrap-detail', args=[trap_id])


class PublicInsectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_super_family_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(SUPERFAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_family_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(FAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sub_family_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(SUBFAMILY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tribe_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(TRIBE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_genus_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(GENUS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_specie_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(SPECIE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_godfather_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(GODFATHER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_trap_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(TRAP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInsectApiTests(TestCase):
    """Test private as user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_trap(self):
        """Test listing trap"""
        sample_insectTrap()
        sample_insectTrap(name='test 2')

        res = self.client.get(TRAP_URL)

        trap = models.InsectTrap.objects.all().order_by('id')
        serializer = serializers.InsectTrapSerializer(
                                        trap,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_trap(self):
        """Test retrieving a trap"""
        trap = sample_insectTrap()

        url = detail_trap_url(trap.id)
        res = self.client.get(url)

        serializer = serializers.InsectTrapSerializer(trap)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_trap_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'trap test name'}

        res = self.client.post(TRAP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_godfather(self):
        """Test listing godfather"""
        sample_insectGodfather()
        sample_insectGodfather(name='test 2')

        res = self.client.get(GODFATHER_URL)

        godfahter = models.InsectGodfather.objects.all().order_by('id')
        serializer = serializers.InsectGodfatherSerializer(
                                        godfahter,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_godfather(self):
        """Test retrieving a super family"""
        godfather = sample_insectGodfather()

        url = detail_godfather_url(godfather.id)
        res = self.client.get(url)

        serializer = serializers.InsectGodfatherSerializer(godfather)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_godfather_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'godfather test name'}

        res = self.client.post(GODFATHER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_super_families(self):
        """Test listing super families"""
        sample_insectSuperFamily()
        sample_insectSuperFamily(name='test 2')

        res = self.client.get(SUPERFAMILY_URL)

        supFamilies = models.InsectSuperFamilies.objects.all().order_by('id')
        serializer = serializers.InsectSuperFamiliesSerializer(
                                        supFamilies,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_super_family(self):
        """Test retrieving a super family"""
        supFamily = sample_insectSuperFamily()

        url = detail_super_family_url(supFamily.id)
        res = self.client.get(url)

        serializer = serializers.InsectSuperFamiliesSerializer(supFamily)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_super_family_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'super family test name'}

        res = self.client.post(SUPERFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_families(self):
        """Test listing families"""
        sample_insectFamily()
        sample_insectFamily(name='test 2')

        res = self.client.get(FAMILY_URL)

        families = models.InsectFamilies.objects.all().order_by('id')
        serializer = serializers.InsectFamiliesSerializer(
                                        families,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_family(self):
        """Test retrieving a family"""
        family = sample_insectFamily()

        url = detail_family_url(family.id)
        res = self.client.get(url)

        serializer = serializers.InsectFamiliesSerializer(family)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_family_admin_required(self):
        """Test admin is required"""
        supFam = sample_insectSuperFamily()
        payload = {'name': 'family test name', 'superFamily': supFam.id}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_sub_families(self):
        """Test listing sub families"""
        sample_insectSubFamily()
        sample_insectSubFamily(name='test 2')

        res = self.client.get(SUBFAMILY_URL)

        subFamilies = models.InsectSubFamilies.objects.all().order_by('id')
        serializer = serializers.InsectSubFamiliesSerializer(
                                        subFamilies,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_sub_family(self):
        """Test retrieving a sub family"""
        subFamily = sample_insectSubFamily()

        url = detail_sub_family_url(subFamily.id)
        res = self.client.get(url)

        serializer = serializers.InsectSubFamiliesSerializer(subFamily)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_sub_family_admin_required(self):
        """Test admin is required"""
        family = sample_insectFamily()
        payload = {'name': 'sub family test name', 'family': family.id}

        res = self.client.post(SUBFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_tribe(self):
        """Test listing tribes"""
        sample_insectTribe()
        sample_insectTribe(name='test 2')

        res = self.client.get(TRIBE_URL)

        tribes = models.InsectTribes.objects.all().order_by('id')
        serializer = serializers.InsectTribesSerializer(
                                        tribes,
                                        many=True
                                    )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_tribe(self):
        """Test retrieving a tribe"""
        tribe = sample_insectTribe()

        url = detail_tribe_url(tribe.id)
        res = self.client.get(url)

        serializer = serializers.InsectTribesSerializer(tribe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tribe_admin_required(self):
        """Test admin is required"""
        subFamily = sample_insectSubFamily()
        payload = {'name': 'tribe test name', 'subFamily': subFamily.id}

        res = self.client.post(TRIBE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_genera(self):
        """Test listing genera"""
        sample_insectGenus()
        sample_insectGenus(name='test 2')

        res = self.client.get(GENUS_URL)

        genera = models.InsectGenera.objects.all().order_by('id')
        serializer = serializers.InsectGeneraSerializer(genera, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_genus(self):
        """Test retrieving a genus"""
        genus = sample_insectGenus()

        url = detail_genus_url(genus.id)
        res = self.client.get(url)

        serializer = serializers.InsectGeneraSerializer(genus)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_genus_admin_required(self):
        """Test admin is required"""
        tribe = sample_insectTribe()
        payload = {'name': 'genus test name', 'tribe': tribe.id}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_species(self):
        """Test listing species"""
        sample_insectSpecie()
        sample_insectSpecie(name='test 2')

        res = self.client.get(SPECIE_URL)

        species = models.InsectSpecies.objects.all().order_by('id')
        serializer = serializers.InsectSpeciesSerializer(species, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_specie(self):
        """Test retrieving a specie"""
        specie = sample_insectSpecie()

        url = detail_specie_url(specie.id)
        res = self.client.get(url)

        serializer = serializers.InsectSpeciesSerializer(specie)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_specie_admin_required(self):
        """Test admin is required"""
        genus = sample_insectGenus()
        payload = {'name': 'specie test name', 'genus': genus.id}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateInsectApiAsAdminTests(TestCase):
    """Test API as admin"""

    def setUp(self):
        self.user = create_superuser(
                        email='admin@ulb.ac.be',
                        password='test123'
                    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_trap(self):
        """Test creating a trap"""
        payload = {'name': 'trap test name'}

        res = self.client.post(TRAP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        trap = models.InsectTrap.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(trap, key))

    def test_create_trap_no_name_fail(self):
        """Test creating a trap without name should fail"""
        payload = {'name': ''}

        res = self.client.post(TRAP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_trap(self):
        """Test updating trap"""
        trap = sample_insectTrap()
        payload = {'name': 'new trap name'}

        url = detail_trap_url(trap.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        trap.refresh_from_db()

        self.assertEqual(trap.name, payload['name'])

    def test_create_godfather(self):
        """Test creating a godfather"""
        payload = {'name': 'godfather test name'}

        res = self.client.post(GODFATHER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        godfather = models.InsectGodfather.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(godfather, key))

    def test_create_godfather_no_name_fail(self):
        """Test creating a godfather without name should fail"""
        payload = {'name': ''}

        res = self.client.post(GODFATHER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_godfather(self):
        """Test updating godfahter"""
        godfather = sample_insectGodfather()
        payload = {'name': 'new godfather name'}

        url = detail_godfather_url(godfather.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        godfather.refresh_from_db()

        self.assertEqual(godfather.name, payload['name'])

    def test_create_super_family(self):
        """Test creating a super family"""
        payload = {'name': 'super family test name'}

        res = self.client.post(SUPERFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        supFamily = models.InsectSuperFamilies.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(supFamily, key))

    def test_create_super_family_no_name_fail(self):
        """Test creating a super family without name should fail"""
        payload = {'name': ''}

        res = self.client.post(SUPERFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_super_family(self):
        """Test updating super family"""
        supFamily = sample_insectSuperFamily()
        payload = {'name': 'new super family name'}

        url = detail_super_family_url(supFamily.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        supFamily.refresh_from_db()

        self.assertEqual(supFamily.name, payload['name'])

    def test_create_family(self):
        """Test creating a family"""
        supFam = sample_insectSuperFamily()
        payload = {'name': 'family test name', 'superFamily': supFam.id}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        family = models.InsectFamilies.objects.get(id=res.data['id'])
        self.assertEqual(family.name, payload['name'])
        self.assertEqual(family.superFamily.id, payload['superFamily'])

    def test_create_family_no_name_fail(self):
        """Test creating a family without name should fail"""
        supFam = sample_insectSuperFamily()
        payload = {'name': '', 'superFamily': supFam.id}

        res = self.client.post(FAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_family(self):
        """Test updating family"""
        family = sample_insectFamily()
        superFamily = sample_insectSuperFamily(name='other super family')
        payload = {'name': 'new family name', 'superFamily': superFamily.id}

        url = detail_family_url(family.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        family.refresh_from_db()

        self.assertEqual(family.name, payload['name'])
        self.assertEqual(family.superFamily.id, payload['superFamily'])

    def test_create_sub_family(self):
        """Test creating a sub family"""
        family = sample_insectFamily()
        payload = {'name': 'family test name', 'family': family.id}

        res = self.client.post(SUBFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        subFamily = models.InsectSubFamilies.objects.get(id=res.data['id'])
        self.assertEqual(subFamily.name, payload['name'])
        self.assertEqual(subFamily.family.id, payload['family'])

    def test_create_sub_family_no_name_fail(self):
        """Test creating a sub family without name should fail"""
        family = sample_insectFamily()
        payload = {'name': '', 'family': family.id}

        res = self.client.post(SUBFAMILY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_sub_family(self):
        """Test updating sub family"""
        subFamily = sample_insectSubFamily()
        family = sample_insectFamily(name='other family')
        payload = {'name': 'new sub family name', 'family': family.id}

        url = detail_sub_family_url(subFamily.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        subFamily.refresh_from_db()

        self.assertEqual(subFamily.name, payload['name'])
        self.assertEqual(subFamily.family.id, payload['family'])

    def test_create_tribe(self):
        """Test creating a tribe"""
        subFamily = sample_insectSubFamily()
        payload = {'name': 'tribe test name', 'subFamily': subFamily.id}

        res = self.client.post(TRIBE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tribe = models.InsectTribes.objects.get(id=res.data['id'])
        self.assertEqual(tribe.name, payload['name'])
        self.assertEqual(tribe.subFamily.id, payload['subFamily'])

    def test_create_tribe_no_name_fail(self):
        """Test creating a tribe without name should fail"""
        subFamily = sample_insectSubFamily()
        payload = {'name': '', 'subFamily': subFamily.id}

        res = self.client.post(TRIBE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_tribe(self):
        """Test updating tribe"""
        tribe = sample_insectTribe()
        subFamily = sample_insectSubFamily(name='other sub family')
        payload = {'name': 'new tribe name', 'subFamily': subFamily.id}

        url = detail_tribe_url(tribe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tribe.refresh_from_db()

        self.assertEqual(tribe.name, payload['name'])
        self.assertEqual(tribe.subFamily.id, payload['subFamily'])

    def test_create_genus(self):
        """Test creating a genus"""
        tribe = sample_insectTribe()
        payload = {'name': 'genus test name', 'tribe': tribe.id}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        genus = models.InsectGenera.objects.get(id=res.data['id'])
        self.assertEqual(genus.name, payload['name'])
        self.assertEqual(genus.tribe.id, payload['tribe'])

    def test_create_genus_no_name_fail(self):
        """Test creating a genus without name should fail"""
        tribe = sample_insectTribe()
        payload = {'name': '', 'tribe': tribe.id}

        res = self.client.post(GENUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_genus(self):
        """Test updating genus"""
        genus = sample_insectGenus()
        tribe = sample_insectTribe(name='other tribe')
        payload = {'name': 'new genus name', 'tribe': tribe.id}

        url = detail_genus_url(genus.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        genus.refresh_from_db()

        self.assertEqual(genus.name, payload['name'])
        self.assertEqual(genus.tribe.id, payload['tribe'])

    def test_create_specie(self):
        """Test creating a specie"""
        genus = sample_insectGenus()
        godfather = sample_insectGodfather()
        payload = {
                    'name': 'specie test name',
                    'genus': genus.id,
                    'godfather': godfather.id,
                    'year': 2010
                }

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        specie = models.InsectSpecies.objects.get(id=res.data['id'])
        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.genus.id, payload['genus'])

    def test_create_specie_no_name_fail(self):
        """Test creating a specie without name should fail"""
        genus = sample_insectGenus()
        payload = {'name': '', 'genus': genus.id}

        res = self.client.post(SPECIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_specie(self):
        """Test updating specie"""
        specie = sample_insectSpecie()
        genus = sample_insectGenus(name='other genus')
        godfather = sample_insectGodfather(name='other godfather')
        payload = {
                    'name': 'new specie name',
                    'genus': genus.id,
                    'godfather': godfather.id
                }

        url = detail_specie_url(specie.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        specie.refresh_from_db()

        self.assertEqual(specie.name, payload['name'])
        self.assertEqual(specie.genus.id, payload['genus'])
