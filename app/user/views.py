from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    rendere_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveUserView(generics.RetrieveAPIView):
    """Retrieve user as authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj


class UpdateUserView(generics.UpdateAPIView):
    """Update user as authenticated user"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get_object(self):
        """Retrieve and return authentication user"""
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj
