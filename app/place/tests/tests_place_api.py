from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_placeType,
        sample_country,
        sample_region,
        sample_city,
        sample_town,
        sample_place,
        sample_project
    )

from place import serializers


PLACETYPE_URL = reverse('place:placetype-list')

COUNTRY_URL = reverse('place:country-list')

REGION_URL = reverse('place:region-list')

CITY_URL = reverse('place:city-list')

TOWN_URL = reverse('place:town-list')

PLACE_URL = reverse('place:place-list')


def detail_placetype_url(placetype_id):
    """Return the detail url for a place type"""
    return reverse('place:placetype-detail', args=[placetype_id])


def detail_country_url(country_id):
    """Return the detail url for a coutry"""
    return reverse('place:country-detail', args=[country_id])


def detail_region_url(region_id):
    """Return the detail url for a region"""
    return reverse('place:region-detail', args=[region_id])


def detail_city_url(city_id):
    """Return the detail url for a city"""
    return reverse('place:city-detail', args=[city_id])


def detail_town_url(town_id):
    """Return the detail url for a town"""
    return reverse('place:town-detail', args=[town_id])


def detail_place_url(place_id):
    """Return the detail url for a place"""
    return reverse('place:place-detail', args=[place_id])


def add_project_place_url(place_id):
    """ Return the url to add a project to a place"""
    return reverse('place:place-add_project', args=[place_id])
#
#
# def remove_project_place_url(place_id):
#     """ Return the url to remove a project to a place"""
#     return reverse('place:place-removeProject', args=[place_id])


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

    def test_region_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(REGION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_city_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(CITY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_town_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(TOWN_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_place_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(PLACE_URL)

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

    def test_list_region(self):
        """Test listing region"""
        sample_region()
        sample_region(name='test 2')
        res = self.client.get(REGION_URL)

        regions = models.Region.objects.all().order_by('id')
        serializer = serializers.RegionSerializer(regions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_region(self):
        """Test retrieving a region"""
        region = sample_region()

        url = detail_region_url(region.id)
        res = self.client.get(url)

        serializer = serializers.RegionSerializer(region)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_region_admin_required(self):
        """Test admin is required"""
        country = sample_country()
        payload = {'name': 'region test name', 'country': country.id}

        res = self.client.post(REGION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_city(self):
        """Test listing city"""
        sample_city()
        sample_city(name='test 2')

        res = self.client.get(CITY_URL)

        citys = models.City.objects.all().order_by('id')
        serializer = serializers.CitySerializer(citys, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_city(self):
        """Test retrieving a city"""
        city = sample_city()

        url = detail_city_url(city.id)
        res = self.client.get(url)

        serializer = serializers.CitySerializer(city)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_city_admin_required(self):
        """Test admin is required"""
        region = sample_region()
        payload = {'name': 'city test name', 'region': region.id}

        res = self.client.post(CITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_town(self):
        """Test listing town"""
        sample_town()
        sample_town(name='test 2')

        res = self.client.get(TOWN_URL)

        towns = models.Town.objects.all().order_by('id')
        serializer = serializers.TownSerializer(towns, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_town(self):
        """Test retrieving a town"""
        town = sample_town()

        url = detail_town_url(town.id)
        res = self.client.get(url)

        serializer = serializers.TownSerializer(town)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_town_admin_required(self):
        """Test admin is required"""
        city = sample_city()
        payload = {'name': 'town test name', 'city': city.id}

        res = self.client.post(TOWN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_place(self):
        """Test listing place"""
        sample_place()
        sample_place(name='test 2')

        res = self.client.get(PLACE_URL)

        places = models.Place.objects.all().order_by('id')
        serializer = serializers.PlaceSerializer(places, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_list_place_with_project(self):
    #     """Test listing place"""
    #     place1 = sample_place()
    #     sample_place(name='test 2')
    #     project = sample_project()
    #     print(vars(project))
    #     place1.projects.add(project)
    #     place1.refresh_from_db()
    #     print(vars(place1.projects.all()))
    #     res = self.client.get(PLACE_URL)
    #
    #     places = models.Place.objects.all().order_by('id')
    #     serializer = serializers.PlaceDeSerializer(places, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_retrieve_place(self):
        """Test retrieving a place"""
        place = sample_place()

        url = detail_place_url(place.id)
        res = self.client.get(url)

        serializer = serializers.PlaceDetailSerializer(place)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_place_admin_required(self):
        """Test admin is required"""
        town = sample_town()
        payload = {'name': 'place test name', 'town': town.id}

        res = self.client.post(PLACE_URL, payload)

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
        """Test updating country"""
        country = sample_country()
        payload = {'name': 'new country name'}

        url = detail_country_url(country.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        country.refresh_from_db()

        self.assertEqual(country.name, payload['name'])

    def test_create_region(self):
        """Test creating a region"""
        country = sample_country()
        payload = {'name': 'region test name', 'country': country.id}

        res = self.client.post(REGION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        region = models.Region.objects.get(id=res.data['id'])
        self.assertEqual(region.name, payload['name'])
        self.assertEqual(region.country.id, payload['country'])

    def test_create_region_no_name_fail(self):
        """Test creating a region without name should fail"""
        payload = {'name': ''}

        res = self.client.post(REGION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_region(self):
        """Test updating region"""
        region = sample_region()
        country = sample_country(name='other country')
        payload = {'name': 'new region name', 'country': country.id}

        url = detail_region_url(region.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        region.refresh_from_db()

        self.assertEqual(region.name, payload['name'])
        self.assertEqual(region.country.id, payload['country'])

    def test_create_city(self):
        """Test creating a city"""
        region = sample_region()
        payload = {'name': 'city test name', 'region': region.id}

        res = self.client.post(CITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        city = models.City.objects.get(id=res.data['id'])
        self.assertEqual(city.name, payload['name'])
        self.assertEqual(city.region.id, payload['region'])

    def test_create_city_no_name_fail(self):
        """Test creating a city without name should fail"""
        payload = {'name': ''}

        res = self.client.post(CITY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_city(self):
        """Test updating city"""
        city = sample_city()
        region = sample_region(name='other region')
        payload = {'name': 'new city name', 'region': region.id}

        url = detail_city_url(city.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        city.refresh_from_db()

        self.assertEqual(city.name, payload['name'])
        self.assertEqual(city.region.id, payload['region'])

    def test_create_town(self):
        """Test creating a town"""
        city = sample_city()
        payload = {'name': 'town test name', 'city': city.id}

        res = self.client.post(TOWN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        town = models.Town.objects.get(id=res.data['id'])
        self.assertEqual(town.name, payload['name'])
        self.assertEqual(town.city.id, payload['city'])

    def test_create_town_no_name_fail(self):
        """Test creating a town without name should fail"""
        payload = {'name': ''}

        res = self.client.post(TOWN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_town(self):
        """Test updating town"""
        town = sample_town()
        city = sample_city(name='other city')
        payload = {'name': 'new town name', 'city': city.id}

        url = detail_town_url(town.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        town.refresh_from_db()

        self.assertEqual(town.name, payload['name'])
        self.assertEqual(town.city.id, payload['city'])

    def test_create_place(self):
        """Test creating a place"""
        town = sample_town()
        type = sample_placeType()
        payload = {
                'name': 'place test name',
                'town': town.id,
                'type': type.id,
                'codeSite': 10,
                'latitudeDec': 10.1,
                'longitudeDec': 9.1
            }

        res = self.client.post(PLACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        place = models.Place.objects.get(id=res.data['id'])
        self.assertEqual(place.name, payload['name'])
        self.assertEqual(place.town.id, payload['town'])

    def test_create_place_no_name_fail(self):
        """Test creating a place without name should fail"""
        payload = {'name': ''}

        res = self.client.post(PLACE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_place(self):
        """Test updating place"""
        place = sample_place()
        town = sample_town(name='other town')
        payload = {'name': 'new place name', 'town': town.id}

        url = detail_place_url(place.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        place.refresh_from_db()

        self.assertEqual(place.name, payload['name'])
        self.assertEqual(place.town.id, payload['town'])

    def test_add_project_to_place(self):
        """Test adding a project to a place"""
        place = sample_place()
        project = sample_project()
        payload = {'project': project.id}

        url = add_project_place_url(place.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        place.refresh_from_db()
        projects = place.projects.all()
        projectSerializer = serializers.ProjectSerializer(projects, many=True)
        self.assertEqual(
                serializers.ProjectSerializer(project)
                .data,
                projectSerializer.data[0]
            )
