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
from Music.models import Style, StyleTitle
from .models import DiscoverTitle

# =================================================================


@api_view(['GET'])
def discover(request, uid=None):
    # 獲取特別專輯
    show_title = ["最近新增", "最新熱門", "台灣歌曲", "韓國歌曲", "日本歌曲", "放克音樂", "金典音樂"]
    super_title_name = ["已發行", "熱門歌曲清單",
                        "好聽的華語抒情歌", "K-RISING",  "J-Hits!", "放克流行金曲", "00 年代琅琅上口的歌曲", ]
    super_list = []

    for name, title in zip(super_title_name, show_title):
        # obj = Style.objects.filter(style_name=name).first()

        DiscoverTitle.objects.create(name=name, show_title=title)

    return Response({"message": "sdsds"})


# @api_view(['GET'])
# def discover(request, uid=None):
#     album_data = AlbumSerializer(
#         Album.objects.all(), many=True).data

#     num_albums = len(album_data)
#     num_groups = (num_albums + 5) // 6  # 计算分组数量

#     superset = []
#     set_title = ["最新上架及熱門歌曲", "台灣音樂", "香港音樂", "K-Pop hits", "J-Pop hits"]

#     for i in range(num_groups):
#         start = i * 6
#         end = min((i + 1) * 6, num_albums)
#         subset = album_data[start:end]

#         album_set = []
#         count = 0
#         for album in subset:
#             count += 1
#             album_set.append(
#                 {'id': i + count, 'album': album})

#         superset.append(
#             {'id': i+100, 'set': album_set, 'title': set_title[i]})

#     return Response(superset)
