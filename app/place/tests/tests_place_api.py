from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_placeType,
    )

from place import serializers


PLACETYPE_URL = reverse('place:placetype-list')


def detail_placetype_url(placetype_id):
    """Return the detail url for a place type"""
    return reverse('place:placetype-detail', args=[placetype_id])


class PublicPlaceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(PLACETYPE_URL)

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

    def test_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'placetype test name'}

        res = self.client.post(PLACETYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
