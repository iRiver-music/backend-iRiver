from django.urls import path, include
from . import views

app_name = 'Music'


urlpatterns = [
    # serch

    #     path('query/db/<str:query>',
    #          views.query_db_song, name='db'),
    #     path('query/web/<str:query>',
    #          views.query_web_song, name='web'),

    #     path('query_style',
    #          views.query_style, name='query_style'),

    #     path('artist/<str:artist>',
    #          views.artist, name='artist'),
    #     path('artist_test/<str:artist>',
    #          views.artist_test, name='artist'),

    #     path('album/<str:album>',
    #          views.album, name='album'),
    #     path('songs/<str:artist>',
    #          views.songs, name='songs'),


    #     # style
    #     path('style/<str:style>/',
    #          views.style, name='style'),
    #     # fail song
    #     path('fail/<str:style>/',
    #          views.style, name='fail'),

    #     # test

    #     path('album/<str:album>/',
    #          views.album, name='album'),
    #     path('songs/<str:artist>/',
    #          views.songs, name='songs'),
    #     path('update_music/', make_json_file, name='update'),
    #     path('test/<str:query>/', query, name='test'),

    #     # change style mdoel
    #     path('change/', views.change, name='change'),
]
