from django.urls import path
from . import views

app_name = 'Track'

urlpatterns = [
    path("init", views.init, name="init"),
    # view

    path("viwes", views.views, name="views"),

    path("music_views", views.music_view, name="music_view"),

    path("search_view", views.search_view, name="search_view"),

    path("artist_view", views.artist_view, name="artist_view"),

    path("song_view", views.song_view, name="song_view"),

    path("fav_view", views.fav_view, name="fav_view"),

    path("tab_view", views.tab_view, name="tab_view"),

    path("device_view", views.device_view, name="device_view"),

    path("register_views", views.register_views, name="register_views"),



    # test
    path("test", views.test, name="test"),


]
