from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.RetrieveUserView.as_view(), name='me'),
    path('user/update/', views.UpdateUserView.as_view(), name='user_update')
]
