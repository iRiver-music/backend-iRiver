from django.urls import path ,include
from . import views

app_name = 'Music'
urlpatterns = [

    path('search/query_db_song/<str:query>/', views.query_db_song, name='query_db_song'),
    path('search/query_web_song/<str:query>/', views.query_web_song, name='query_web_song'),
    path('get_artist_info/<str:artist>/', views.get_artist_info, name='get_artist_info'),
    path('search/query_album/<str:be_search_album>/', views.query_album, name='query_album'), 
]