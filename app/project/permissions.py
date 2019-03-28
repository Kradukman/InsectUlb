from rest_framework import permissions
from core import models


class CanAccessProject(permissions.BasePermission):
    """permission if user is active, leader or admin on a project"""

    def has_object_permission(self, request, obj, view):
        pk = request.resolver_match.kwargs.get('pk')
        project = models.Project.objects.get(id=pk)
        is_active = False
        if request.user.is_staff:
            return True
        if project.projectLeader == request.user:
            return True
        try:
            is_active = models.ProjectMembership.objects.get(
                                        user=request.user,
                                        project=project
                                    ).is_active
        except models.ProjectMembership.DoesNotExist:
            print('error')
        return is_active
