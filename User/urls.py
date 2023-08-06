from django.urls import path,include
from User.model.EQAPIView import EQAPIView
from User.model.PlaylistAPIView import PlaylistAPIView
from User.model.ProfileAPIView import ProfileAPIView
from User.model.SettingAPIView import SettingAPIView
from User.model.UserAPIView import UserAPIView
from User.model.MyPlayListAPIView import MyPlayListAPIView
from User.model.UserLoginAPIView import UserLoginAPIView
from . import views

# 異步版本
from drfa.decorators import api_view,APIView
from asgiref.sync import sync_to_async

# rest_framework
from rest_framework import generics
from rest_framework.response import Response

app_name="User"
urlpatterns=[
    # 檢查邀請碼
    path('valid_invitation_code/<str:invitation_code>/',views.valid_invitation_code,name='valid_invitation_code'),

    path("logout/<str:uid>/",views.logout,name="logout"), # 登出
    path("login/",UserLoginAPIView.as_view(),name="login"),

    path("listeningHistory/<str:music_ID>/",views.listeningHistory,name="listeningHistory"), # 紀錄播放紀錄
    path("my_playList/<str:uid>/",MyPlayListAPIView.as_view(),name="my_playList"),

    path("<str:uid>/",UserAPIView.as_view(),name="user"), # 獲取帳號資訊 刪除帳號

    path("setting/<str:uid>/",SettingAPIView.as_view(),name="setting"), # 設定
    path("eq/<str:uid>/",EQAPIView.as_view(),name="eq"), # eq設定
    path("profile/<str:uid>/",ProfileAPIView.as_view(),name="profile"), # 個人檔案設定

    path("playlist/<str:uid>/<str:playlist>/",PlaylistAPIView.as_view(),name="playlist"),
    path("playlist/<str:uid>/",PlaylistAPIView.as_view(),name="playlist"),
]
