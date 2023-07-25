from django.urls import path, include
from . import views

app_name = 'Music'
urlpatterns = [

    path('query/db/<str:query>/',
         views.query_db_song, name='db'),
    path('query/web/<str:query>/',
         views.query_web_song, name='web'),
    path('artist/<str:artist>/',
         views.artist, name='artist'),
    path('album/<str:album>/',
         views.album, name='album'),
    path('songs/<str:artist>/',
         views.songs, name='songs'),
]
