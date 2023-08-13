from django.shortcuts import render
from Music.models import Album, Song
from urllib import response

from Music.serializers import AlbumSerializer, SongSerializer

# 異步版本
from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async

# 異步
import concurrent.futures

# rest_framework
from rest_framework import generics
from rest_framework.response import Response

# models
from Music.models import Style
from User.model.PlaylistAPIView import get_uid_fav_song
from User.models import Playlist
from .models import DiscoverTitle

# =================================================================


@api_view(['GET'])
def discover(request, uid=None):
    obj = DiscoverTitle.objects.all().values()

    playlist = []
    # fav
    if Playlist.objects.filter(uid=uid,  playlist="fav").exists():
        playlist.append({"title": "我的最愛", "name": "fav",
                         "data": get_uid_fav_song(uid)})

    for discover in obj:
        obj_song_data = Style.objects.filter(
            style=discover["name"]).values()

        data = SongSerializer(obj_song_data, many=True).data
        playlist.append({"title": discover['show_title'], "name": discover["name"],
                         "data": data})

    return Response(playlist)


@api_view(['GET'])
def push_discover(request, uid=None):
    # 獲取特別專輯
    show_title = ["最近新增", "最新熱門", "台灣歌曲", "韓國歌曲", "日本歌曲", "放克音樂", "金典音樂"]
    super_title_name = ["已發行", "熱門歌曲清單",
                        "好聽的華語抒情歌", "K-RISING",  "J-Hits!", "放克流行金曲", "00 年代琅琅上口的歌曲", ]
    super_list = []

    for name, title in zip(super_title_name, show_title):
        # obj = Style.objects.filter(style_name=name).first()

        DiscoverTitle.objects.create(name=name, show_title=title)

    return Response({"message": "sdsds"})
