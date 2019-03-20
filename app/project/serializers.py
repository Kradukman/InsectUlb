from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects"""
    projectLeader = serializers.PrimaryKeyRelatedField(
                            many=False, queryset=get_user_model().objects.all()
                        )

    class Meta:
        model = Project
        fields = (
                    'id',
                    'name',
                    'abreviation',
                    'beginYear',
                    'endYear',
                    'description',
                    'projectLeader'
                )
        read_only_fields = ('id',)
        required_fields = ('name', 'beginYear', 'projectLeader')
