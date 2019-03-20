from core.views import BasePermissionsViewset

from core.models import Project

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
