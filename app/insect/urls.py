from django.urls import path, include
from rest_framework.routers import DefaultRouter

from insect import views


app_name = 'insect'

router = DefaultRouter()
router.register('superfamilies', views.InsectSuperFamiliesViewset)
router.register('families', views.InsectFamiliesViewset)
router.register('subfamilies', views.InsectSubFamiliesViewset)
router.register('tribes', views.InsectTribesViewset)
router.register('genes', views.InsectGenesViewset)
router.register('species', views.InsectSpeciesViewset)

urlpatterns = [
    path('', include(router.urls)),
]
