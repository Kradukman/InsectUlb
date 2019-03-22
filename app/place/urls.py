from django.urls import path, include
from rest_framework.routers import DefaultRouter

from place import views


app_name = 'place'

router = DefaultRouter()
router.register('placetype', views.PlaceTypeViewset)
router.register('country', views.CountryViewset)
router.register('region', views.RegionViewset)
router.register('city', views.CityViewset)
router.register('town', views.TownViewset)
router.register('place', views.PlaceViewset)


urlpatterns = [
    path('', include(router.urls)),
]
