from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views


app_name = 'user'

router = DefaultRouter()
router.register('user', views.UserViewset)

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.RetrieveUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
