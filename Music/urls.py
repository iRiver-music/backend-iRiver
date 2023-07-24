from django.urls import path ,include
from . import views

app_name = 'Music'
urlpatterns = [

    path('query_db_song/', views.query_db_song, name='query_db_song'),
    path('query_web_song/', views.query_web_song, name='query_web_song'),
    path('get_artist_info/', views.get_artist_info, name='get_artist_info'),

]