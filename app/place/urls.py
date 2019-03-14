from django.urls import path, include
from rest_framework.routers import DefaultRouter

from place import views


app_name = 'place'

router = DefaultRouter()
router.register('placetype', views.PlaceTypeViewset)

urlpatterns = [
    path('', include(router.urls)),
]
