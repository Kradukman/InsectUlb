from django.shortcuts import get_object_or_404

from core.views import BasePermissionsViewset
from core.models import Project

from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from project.permissions import CanAccessProject
from project import serializers


class ProjectViewset(BasePermissionsViewset):
    """Manage project as admin"""
    serializer_class = serializers.ProjectSerializer
    queryset = Project.objects.all()

    # def create(self, request, *args, **kwargs):
    #     print('in viewset create')
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     print('\n is valid: ')
    #     serializer.is_valid()
    #     print(serializer.errors)
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.action in ['list', 'retrieve', ]:
            self.permission_classes = [
                        permissions.IsAuthenticated,
                        CanAccessProject,
                    ]
        if self.action in [
            'create',
            'update',
            'partial_update',
            'add_project',
            'remove_project',
            'update_attribute',
            'assign_place'
        ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action in [
            'retrieve',
            'assign_user',
            'assign_place'
        ]:
            return serializers.ProjectDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if self.action == 'list':
            if not self.request.user.is_staff:
                queryset = (
                        Project.objects.filter(projectLeader=user)
                        |
                        Project.objects.filter(members=user)
                    )
        return queryset

    @action(
        methods=['patch'],
        detail=True,
        url_path='assign-user',
        url_name='assign_user'
    )
    def assign_user(self, request, pk=None):
        response = {}
        # get serializer
        serializer = self.get_serializer()
        project = serializer.assign_user(
                project_id=pk,
                user_id=self.request.data['user_id']
            )
        projectSerializer = serializers.ProjectDetailSerializer(project)
        response['data'] = projectSerializer.data
        return Response(response)

    @action(
        methods=['patch'],
        detail=True,
        url_path='assign-place',
        url_name='assign_place'
    )
    def assign_place(self, request, pk=None):
        response = {}
        # get serializer
        serializer = self.get_serializer()
        project = serializer.assign_place(
                project_id=pk,
                place_id=self.request.data['place_id']
            )
        projectSerializer = serializers.ProjectDetailSerializer(project)
        response['data'] = projectSerializer.data
        return Response(response)
