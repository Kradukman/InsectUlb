from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project import views


app_name = 'project'

router = DefaultRouter()
router.register('project', views.ProjectViewset)

urlpatterns = [
    path('', include(router.urls)),
]
