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
# =================================================================


@api_view(['GET'])
def web_discover(request, uid=None):
    # 獲取特別專輯
    title = ["最新上架及熱門歌曲", "台灣音樂", "香港音樂", "K-Pop hits", "J-Pop hits"]
    style = ["J-Rock!", "放克流行金曲"]
    song_style = ["us-pop", "tw-pop"]
    style_super_set = StyleTitle.objects.all().values()
    return


@api_view(['GET'])
def phone_discover(request, uid=None):
    # 所有曲風
    pass


@api_view(['GET'])
def discover(request):
    album_data = AlbumSerializer(
        Album.objects.all(), many=True).data

    num_albums = len(album_data)
    num_groups = (num_albums + 5) // 6  # 计算分组数量

    superset = []
    set_title = ['為你推薦', '10大排行榜', '大家都在聽', '10大排行榜', '為你推薦', '10大排行榜']

    for i in range(num_groups):
        start = i * 6
        end = min((i + 1) * 6, num_albums)
        subset = album_data[start:end]

        album_set = []
        count = 0
        for album in subset:
            count += 1
            album_set.append(
                {'id': i + count, 'album': album})

        superset.append(
            {'id': i+100, 'set': album_set, 'title': set_title[i]})

    return Response(superset)
