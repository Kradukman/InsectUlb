from django.urls import path, include
from rest_framework.routers import DefaultRouter

from insect import views


app_name = 'insect'

router = DefaultRouter()
router.register('superfamilies', views.InsectSuperFamiliesViewset)
router.register('families', views.InsectFamiliesViewset)
router.register('subfamilies', views.InsectSubFamiliesViewset)
router.register('tribes', views.InsectTribesViewset)
router.register('genus', views.InsectGeneraViewset)
router.register('species', views.InsectSpeciesViewset)
router.register('godfather', views.InsectGodfatherViewset)
router.register('trap', views.InsectTrapViewset)

urlpatterns = [
    path('', include(router.urls)),
]
