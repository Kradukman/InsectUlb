from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_placeType,
        sample_country
    )

from place import serializers


PLACETYPE_URL = reverse('place:placetype-list')

COUNTRY_URL = reverse('place:country-list')


def detail_placetype_url(placetype_id):
    """Return the detail url for a place type"""
    return reverse('place:placetype-detail', args=[placetype_id])


def detail_country_url(country_id):
    """Return the detail url for a coutry"""
    return reverse('place:country-detail', args=[country_id])


class PublicPlaceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_placetype_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(PLACETYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(COUNTRY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlaceApiTests(TestCase):
    """Test private as user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_placetype(self):
        """Test listing place type"""
        sample_placeType()
        sample_placeType(name='test 2')

        res = self.client.get(PLACETYPE_URL)

        placetypes = models.PlaceType.objects.all().order_by('id')
        serializer = serializers.PlaceTypeSerializer(placetypes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_placetype(self):
        """Test retrieving a placetype"""
        placetype = sample_placeType()

        url = detail_placetype_url(placetype.id)
        res = self.client.get(url)

        serializer = serializers.PlaceTypeSerializer(placetype)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_placetype_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'placetype test name'}

        res = self.client.post(PLACETYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_country(self):
        """Test listing countries"""
        sample_country()
        sample_country(name='test 2')

        res = self.client.get(COUNTRY_URL)

        countries = models.Country.objects.all().order_by('id')
        serializer = serializers.CountrySerializer(countries, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_country(self):
        """Test retrieving a country"""
        country = sample_country()

        url = detail_country_url(country.id)
        res = self.client.get(url)

        serializer = serializers.CountrySerializer(country)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_country_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'country test name'}

        res = self.client.post(COUNTRY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePlaceApiAsAdminTests(TestCase):
    """Test API as admin"""

    def setUp(self):
        self.user = create_superuser(
                        email='admin@ulb.ac.be',
                        password='test123'
                    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_placetype(self):
        """Test creating a place type"""
        payload = {'name': 'place type test name'}

        res = self.client.post(PLACETYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        family = models.PlaceType.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(family, key))

    def test_create_placetype_no_name_fail(self):
        """Test creating a place type without name should fail"""
        payload = {'name': ''}

        res = self.client.post(PLACETYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_placetype(self):
        """Test updating family"""
        placeType = sample_placeType()
        payload = {'name': 'new place type name'}

        url = detail_placetype_url(placeType.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        placeType.refresh_from_db()

        self.assertEqual(placeType.name, payload['name'])

    def test_create_country(self):
        """Test creating a country"""
        payload = {'name': 'country test name'}

        res = self.client.post(COUNTRY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        country = models.Country.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(country, key))

    def test_create_country_no_name_fail(self):
        """Test creating a country without name should fail"""
        payload = {'name': ''}

        res = self.client.post(COUNTRY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_country(self):
        """Test updating family"""
        country = sample_country()
        payload = {'name': 'new country name'}

        url = detail_country_url(country.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        country.refresh_from_db()

        self.assertEqual(country.name, payload['name'])
