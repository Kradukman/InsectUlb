from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core import models
from user.tests.test_user_api import create_superuser
from core.tests.test_models import (
        sample_project,
        sample_user
    )

from project import serializers


PROJECT_URL = reverse('project:project-list')


def detail_project_url(project_id):
    """Return the detail url for a place type"""
    return reverse('project:project-detail', args=[project_id])


def assign_user_project_url(project_id):
    """Return the url to assign a user to a project"""
    return reverse('project:project-assign_user', args=[project_id])


class PublicPlaceApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_placetype_auth_required(self):
        """Test authentification is required"""
        res = self.client.get(PROJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePlaceApiTests(TestCase):
    """Test private as user"""

    def setUp(self):
        self.user = sample_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_project(self):
        """Test listing projects"""
        projectLeader = sample_user(email='techlead@ulb.ac.be')
        sample_project(projectLeader=projectLeader)
        sample_project(name='test 2', projectLeader=projectLeader)

        res = self.client.get(PROJECT_URL)

        projects = models.Project.objects.all().order_by('id')
        serializer = serializers.ProjectSerializer(projects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_project_as_member(self):
        """Test retrieving a project as a member of the project"""
        project = sample_project()
        models.ProjectMembership.objects.create(
                            user=self.user,
                            project=project,
                            is_active=True
                        )

        url = detail_project_url(project.id)
        res = self.client.get(url)

        serializer = serializers.ProjectDetailSerializer(project)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_project_admin_required(self):
        """Test admin is required"""
        payload = {'name': 'project test name'}

        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_project_fail_inactive_user(self):
        """Test is_active in project membership required"""
        user = sample_user(email='sample2@ulb.ac.be')
        project = sample_project(name='my super test', projectLeader=user)
        models.ProjectMembership.objects.create(
                user=self.user,
                project=project,
                is_active=False
            )
        url = detail_project_url(project.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateProjectApiAsAdminTests(TestCase):
    """Test API as admin"""

    def setUp(self):
        self.user = create_superuser(
                        email='admin@ulb.ac.be',
                        password='test123'
                    )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_project(self):
        """Test creating a project"""
        payload = {
                'name': 'project test name',
                'projectLeader': self.user.id,
                'abreviation': 'ptn-244',
                'beginYear': 2010
            }
        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        project = models.Project.objects.get(id=res.data['id'])
        self.assertEqual(project.name, payload['name'])
        self.assertEqual(
                project.projectLeader.id,
                payload['projectLeader']
            )
        self.assertEqual(project.beginYear, payload['beginYear'])

    def test_create_project_no_name_fail(self):
        """Test creating a project without name should fail"""
        payload = {'name': ''}

        res = self.client.post(PROJECT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_project(self):
        """Test updating project"""
        project = sample_project()
        projectLeader = sample_user(
                            email='otherTest@ulb.ac.be',
                            name='other leader'
                        )
        payload = {
                'name': 'new project name',
                'projectLeader': projectLeader.id,
            }

        url = detail_project_url(project.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()

        self.assertEqual(project.name, payload['name'])
        self.assertEqual(
                project.projectLeader.id,
                payload['projectLeader']
            )

    def test_retrieve_project_as_admin(self):
        """Test retrieving a project"""
        projectLeader = sample_user(email='otherTest@ulb.ac.be')
        project = sample_project(projectLeader=projectLeader)

        url = detail_project_url(project.id)
        res = self.client.get(url)

        serializer = serializers.ProjectDetailSerializer(project)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_assign_user_to_project(self):
        """Test assign user to a project"""
        project = sample_project(projectLeader=self.user)
        user = sample_user(email="legolas@ulb.ac.be")

        payload = {'user_id': user.id}
        url = assign_user_project_url(project.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertIn(user, project.members.all())
