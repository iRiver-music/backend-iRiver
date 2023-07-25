from django.urls import path, include
from . import views

app_name = 'Discover'

urlpatterns = [
    path('',
         views.discover, name='discover'),
]
