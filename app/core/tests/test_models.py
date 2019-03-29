from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from core import models


def sample_plantFamily(name='test family'):
    return models.PlantFamilies.objects.get_or_create(name=name)[0]


def sample_plantGene(name='test Gene', family=None):
    if family is None:
        family = sample_plantFamily()
    return models.PlantGenes.objects.get_or_create(name=name, family=family)[0]


def sample_plantSpecie(name='test specie', gene=None):
    if gene is None:
        gene = sample_plantGene()
    return models.PlantSpecies.objects.get_or_create(name=name, gene=gene)[0]


def sample_placeType(name='test place type'):
    return models.PlaceType.objects.get_or_create(name=name)[0]


def sample_country(name='test country'):
    return models.Country.objects.get_or_create(name=name)[0]


def sample_region(name='test region', country=None):
    if country is None:
        country = sample_country()
    return models.Region.objects.get_or_create(name=name, country=country)[0]


def sample_city(name='test city', region=None):
    if region is None:
        region = sample_region()
    return models.City.objects.get_or_create(name=name, region=region)[0]


def sample_town(name='test town', city=None):
    if city is None:
        city = sample_city()
    return models.Town.objects.get_or_create(name=name, city=city)[0]


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def sample_user(
                    email='sampletest@ulb.ac.be',
                    password='testpass123',
                    name='test1'
                ):
    try:
        user = get_user_model().objects.get(email=email)
        return user
    except ObjectDoesNotExist:
        return create_user(email=email, password=password, name=name)


def sample_project(name='test project', projectLeader=None):
    if projectLeader is None:
        projectLeader = sample_user()
    beginYear = 2010
    return models.Project.objects.get_or_create(
            name=name,
            projectLeader=projectLeader,
            beginYear=beginYear)[0]


def sample_place(
                    name='test place',
                    type=None,
                    codeSite='code site',
                    latitudeDec=11.2,
                    longitudeDec=-32.99,
                    town=None,
                ):
    if type is None:
        type = sample_placeType()
    if town is None:
        town = sample_town()
    return models.Place.objects.get_or_create(
            name=name,
            type=type,
            codeSite=codeSite,
            town=town,
            longitudeDec=longitudeDec,
            latitudeDec=latitudeDec
        )[0]


def sample_insectSuperFamily(name='test insect super family'):
    return models.InsectSuperFamilies.objects.get_or_create(name=name)[0]


def sample_insectFamily(name='test insect family', insectSupFam=None):
    if insectSupFam is None:
        insectSupFam = sample_insectSuperFamily()
    return models.InsectFamilies.objects.get_or_create(
                                    name=name,
                                    superFamily=insectSupFam
                                )[0]


def sample_insectSubFamily(name='test sub family', insectFam=None):
    if insectFam is None:
        insectFam = sample_insectFamily()
    return models.InsectSubFamilies.objects.get_or_create(
                                    name=name,
                                    family=insectFam
                                )[0]


def sample_insectTribe(name='test tribe', insectSubFam=None):
    if insectSubFam is None:
        insectSubFam = sample_insectSubFamily()
    return models.InsectTribes.objects.get_or_create(
                                    name=name,
                                    subFamily=insectSubFam
                                )[0]


def sample_insectGene(name='test genus', insectTribe=None):
    if insectTribe is None:
        insectTribe = sample_insectTribe()
    return models.InsectGenes.objects.get_or_create(
                                    name=name,
                                    tribe=insectTribe
                                )[0]


def sample_insectSpecie(name='test specie', insectGen=None):
    if insectGen is None:
        insectGen = sample_insectGene()
    return models.InsectSpecies.objects.get_or_create(
                                    name=name,
                                    gene=insectGen
                                )[0]


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
