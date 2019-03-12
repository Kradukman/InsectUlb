from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
UPDATE_URL = reverse('user:user_update')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class PublicUserApiTests(TestCase):
    """Test the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_not_connected(self):
        """Test creating a user without identification"""
        payload = {'email': 'test@ulb.ac.be', 'password': 'test123'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@ulb.ac.be', 'password': 'pass123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credential are given"""
        create_user(email='test@ulb.ac.be', password='password123')
        payload = {'email': 'test@ulb.ac.be', 'password': 'wrong'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crete_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@ulb.ac.be', 'password': 'testpass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API request that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@ulb.ac.be',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user_connected_not_admin(self):
        """Test create a user without being admin"""
        payload = {
            'email': 'test2@ulb.ac.be',
            'password': 'test123',
            'name': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_profile_success(self):
        """Test retrieving a profile for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_fail(self):
        """Test updating the user profile for admin"""
        payload = {'name': 'new name', 'password': 'newpassword123'}
        res = self.client.patch(UPDATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateUserAPIAdminTests(TestCase):
    """Test API if user is admin"""

    def setUp(self):
        self.user = create_superuser(
            email='testAdmin@ulb.ac.be',
            password='testpass',
            name='admin name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_user_if_admin(self):
        """Test that admin can create user"""
        payload = {
            'email': 'test2@ulb.ac.be',
            'password': 'pass1234',
            'name': 'test name'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_update_user_profile(self):
        """Test updating the user profile for admin"""
        payload = {'name': 'new name', 'password': 'newpassword123'}
        res = self.client.patch(UPDATE_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # Test create USER
    # create super USER
    # force login
    # create USER
    # user should be created
    # test permission in serializer
    # test create user without superuser
    # should not create user
