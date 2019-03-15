from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_plantFamily(name='test family'):
    return models.PlantFamilies.objects.create(name=name)


def sample_plantGene(name='test Gene', family=None):
    if family is None:
        family = sample_plantFamily()
    return models.PlantGenes.objects.create(name=name, family=family)


def sample_plantSpecie(name='test specie', gene=None):
    if gene is None:
        gene = sample_plantGene()
    return models.PlantSpecies.objects.create(name=name, gene=gene)


def sample_placeType(name='test place type'):
    return models.PlaceType.objects.create(name=name)


def sample_country(name='test country'):
    return models.Country.objects.create(name=name)


def sample_region(name='test region', country=None):
    if country is None:
        country = sample_country()
    return models.Region.objects.create(name=name, country=country)


def sample_city(name='test city', region=None):
    if region is None:
        region = sample_region()
    return models.City.objects.create(name=name, region=region)


def sample_town(name='test town', city=None):
    if city is None:
        city = sample_city()
    return models.Town.objects.create(name=name, city=city)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@ulb.ac.be'
        password = 'Testpassword123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email  for a user is normalized"""
        email = 'test@ULB.AC.BE'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Test creating a user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@ulb.ac.be',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_baseModel_str(self):
        """Test the BaseModel string representation.
        Since abstract, juste use a class with direct inheritance."""
        baseModel = sample_plantFamily()

        self.assertEqual(str(baseModel), baseModel.name)
