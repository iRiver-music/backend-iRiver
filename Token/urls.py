from django.urls import path ,include
from . import views

app_name = 'Token'
urlpatterns = [
    path('token/', views.get_csrf_token, name='get_token'),
    path('token/api', views.some_api_endpoint, name='api_endpoint'),
]