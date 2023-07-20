from django.urls import path ,include
from . import views

app_name = 'Music'
urlpatterns = [
    path('my_music_list/', views.my_music_list, name='my_music_list'),
    path('search/', views.search, name=' search'),
    path('query_db_song/', views.query_db_song, name='query_db_song'),
    path('query_web_song/', views.query_web_song, name='query_web_song'),
    path('get_music_list/', views.get_music_list, name='get_music_list'),
    path('music_list/', views.music_list, name='music_list'),
    

]