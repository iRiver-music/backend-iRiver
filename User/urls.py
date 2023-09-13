from django.urls import path, include
from User.model.EQAPIView import EQAPIView
from User.model.PlaylistAPIView import PlaylistAPIView
from User.model.ProfileAPIView import ProfileAPIView
from User.model.SettingAPIView import SettingAPIView
from User.model.UserAPIView import UserAPIView
from User.model.MyPlayListAPIView import MyPlayListAPIView
from . import views
# rate
from django_ratelimit.decorators import ratelimit

# 異步版本
from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async

# rest_framework
from rest_framework import generics
from rest_framework.response import Response

app_name = "User"
urlpatterns = [
    # HIS
    path("listeningHistory/<str:music_ID>",
         views.listeningHistory, name="listeningHistory"),
    path("searchHistory/<str:uid>/<str:query>",
         views.searchHistory, name="SearchHistory"),


    path("my_playList/<str:uid>", MyPlayListAPIView.as_view(), name="my_playList"),


    path("setting/<str:uid>", SettingAPIView.as_view(), name="setting"),  # 設定

    path("eq/<str:uid>", EQAPIView.as_view(), name="eq"),  # eq設定

    path("profile/<str:uid>", ProfileAPIView.as_view(), name="profile"),  # 個人檔案設定

    path("playlist/<str:uid>/<str:playlist>",
         PlaylistAPIView.as_view(), name="playlist"),
    path("playlist/<str:uid>", PlaylistAPIView.as_view(), name="playlist"),

    # get playlist title
    path("playlistSet/<str:uid>", views.playlistSet, name="playlistSet"),
    #     song
    path("playlistSet/song/<str:uid>/<playlist:str>",
         views.playlistSet_song, name="playlistSet"),

    # get user music_ID
    path("music_ID/<str:uid>", views.music_ID, name="music_ID"),

    # last user song
    path("lastUserSong/<str:uid>",
         views.LastuserSongAPIView.as_view(), name="userSong"),


    # test
    path("creat_test",
         views.creat_test_user, name="creat_test"),  # 紀錄播放紀錄

    # playlist img

    path("img/<str:uid>/<str:playlist>",
         views.user_playlist_img, name="user_playlist_img"),
    # 必須放最後一個
    path("<str:uid>", UserAPIView.as_view(), name="user"),  # 獲取帳號資訊 刪除帳號
]
