from rest_framework import viewsets, authentication, permissions


class BasePermissionsViewset(viewsets.ModelViewSet):
    """Base viewset to manage models. \
        Admin can create/update, user can list/retrieve"""
    authentication_classes = (authentication.TokenAuthentication, )

    def get_permissions(self):
        if self.action in ['list', 'retrieve', ]:
            self.permission_classes = [permissions.IsAuthenticated, ]
        if self.action in ['create', 'update', 'partial_update', ]:
            self.permission_classes = [permissions.IsAdminUser, ]
        return [permission() for permission in self.permission_classes]
