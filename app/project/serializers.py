from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import (
                    Project,
                    ProjectMembership,
                    Place
                )

from user.serializers import UserSerializer

from place.serializers import PlaceDetailSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""
    projectLeader = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=get_user_model().objects.all()
                        )
    # members = serializers.PrimaryKeyRelatedField(
    #                         many=True,
    #                         queryset=ProjectMembership.objects.all())
    places = serializers.PrimaryKeyRelatedField(
                            many=True, queryset=Place.objects.all()
                        )

    class Meta:
        model = Project
        fields = (
                    'id',
                    'name',
                    'places',
                    'abreviation',
                    'beginYear',
                    'endYear',
                    'description',
                    'projectLeader'
                )
        read_only_fields = ('id',)
        required_fields = ('name', 'beginYear', 'projectLeader')


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for membership relationship"""
    user = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=get_user_model().objects.all()
                        )
    project = serializers.PrimaryKeyRelatedField(
                            many=False,
                            queryset=Project.objects.all()
                        )

    class Meta:
        model = ProjectMembership
        fields = ('user', 'project',)


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for project object"""
    projectLeader = UserSerializer(many=False)
    members = UserSerializer(many=True)
    places = PlaceDetailSerializer(many=True)

    class Meta:
        model = Project
        fields = (
                    'id',
                    'name',
                    'members',
                    'places',
                    'abreviation',
                    'beginYear',
                    'endYear',
                    'description',
                    'projectLeader'
                )
        read_only_fields = ('id',)
        required_fields = ('name', 'beginYear', 'projectLeader')

    def create(self):
        pass

    def assign_user(self, project_id, user_id):
        project = Project.objects.get(id=project_id)
        user = get_user_model().objects.get(id=user_id)
        ProjectMembership.objects.create(
                                user=user,
                                project=project,
                                is_active=True
                            )
        return project

    def assign_place(self, project_id, place_id):
        project = Project.objects.get(id=project_id)
        place = Place.objects.get(id=place_id)
        project.places.add(place)
        return project
