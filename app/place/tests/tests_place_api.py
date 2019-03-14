from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser, sample_user
from core.tests.test_models import (
        sample_placeType,
    )

#from place import serializers


#PLACETYPE_URL = reverse('place:placetype-list')
