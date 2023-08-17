from django.urls import path, include
from . import views
from Music.music_db.writeJson import make_json_file
from Music.query import new_query

app_name = 'Music'


urlpatterns = [

    path('query/db/<str:query>/',
         views.query_db_song, name='db'),
    path('query/web/<str:query>/',
         views.query_web_song, name='web'),
    path('artist/<str:artist>/',
         views.artist, name='artist'),
    path('artist_test/<str:artist>/',
         views.artist_test, name='artist'),

    path('album/<str:album>/',
         views.album, name='album'),
    path('songs/<str:artist>/',
         views.songs, name='songs'),


    # style
    path('style/<str:style>/',
         views.style, name='style'),
    # test

    path('album/<str:album>/',
         views.album, name='album'),
    path('songs/<str:artist>/',
         views.songs, name='songs'),
    path('update_music/', make_json_file, name='update'),
    path('test/<str:query>/', new_query, name='test'),

    # change style mdoel
    path('change/', views.change, name='change'),
]
