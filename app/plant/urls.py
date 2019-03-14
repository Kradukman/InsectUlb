from django.urls import path, include
from rest_framework.routers import DefaultRouter

from plant import views


app_name = 'plant'

router = DefaultRouter()
router.register('family', views.PlantFamiliesViewset)
router.register('gene', views.PlantGenesViewset)
router.register('specie', views.PlantSpeciesViewset)

urlpatterns = [
    path('', include(router.urls)),
]
