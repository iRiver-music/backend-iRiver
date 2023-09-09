from django.urls import path, include
from . import views

app_name = 'Token'
urlpatterns = [
    path('get_container_stats/', views.get_container_stats,
         name='get_container_stats'),
]
