from django.urls import path ,include
from . import views
from .views import UserTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'Token'
urlpatterns = [
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]