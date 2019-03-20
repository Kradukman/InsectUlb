from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from user.serializers import UserSerializer

from core.tests.test_models import (
            create_user,
            create_superuser,
            sample_user
        )


TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
USER_URL = reverse('user:user-list')


def detail_url(user_id):
    """Return user detail URL"""
    return reverse('user:user-detail', args=[user_id])


class PublicUserApiTests(TestCase):
    """Test the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(USER_URL)

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

    def test_create_token_no_user(self):
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

    def test_admin_required(self):
        """Test authentification is required"""
        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_profile_success(self):
        """Test retrieving a profile for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email,
            'is_active': self.user.is_active
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


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

    def test_retrieve_users(self):
        """Test listing user for admin"""
        sample_user()
        sample_user(email='test2@ulb.ac.be', name='test2')
        res = self.client.get(USER_URL)

        users = get_user_model().objects.all().order_by('id')
        serializer = UserSerializer(users, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_user_detail(self):
        user = sample_user()

        url = detail_url(user.id)
        res = self.client.get(url)

        serializer = UserSerializer(user)
        self.assertEqual(res.data, serializer.data)

    def test_create_user_if_admin(self):
        """Test that admin can create user"""
        payload = {
            'email': 'test2@ulb.ac.be',
            'password': 'pass1234',
            'name': 'test name'}
        res = self.client.post(USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(id=res.data['id'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertEqual(user.name, res.data['name'])
        self.assertEqual(user.is_active, res.data['is_active'])
        self.assertEqual(user.email, res.data['email'])

    def test_full_update_user(self):
        """Test updating the user profile for admin"""
        user = sample_user()
        payload = {
            'id': user.id,
            'name': 'new name',
            'password': 'newpassword123',
            'is_active': 'False'
        }
        url = detail_url(user.id)
        res = self.client.patch(url, payload)

        user.refresh_from_db()

        self.assertEqual(user.name, payload['name'])
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
