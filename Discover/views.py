from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render
from Discover.serializers import DiscoverTitleSerializer, StyleTitleSerializer
from Music.models import Album, Song, StyleTitle
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
# rate_limit
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

# =================================================================


@api_view(['GET'])
@ratelimit(key=settings.RATELIMIT_KEY, rate=settings.RATELIMITS_DEFAULT)
def discover(request, uid):
    obj = DiscoverTitle.objects.all().values()

    playlist = []
    id = 10000
    # fav
    if Playlist.objects.filter(uid=uid,  playlist="fav").exists():
        songs = get_uid_fav_song(uid)
        if len(songs) > 0:
            playlist.append({"id": id, "title": "我的最愛", "style": "fav",
                            "songs": songs})

    for discover in obj:
        obj_song_data = Style.objects.filter(
            style=discover["name"]).values()

        data = SongSerializer(obj_song_data, many=True).data
        id = id + 1
        playlist.append({"id": id,  "title": discover['show_title'], "style": discover["name"],
                         "songs": data})

    return Response(playlist)


# @api_view(['GET'])
# def push_discover(request, uid=None):
#     # 獲取特別專輯
#     show_title = ["最近新增", "最新熱門", "台灣歌曲", "韓國歌曲", "日本歌曲", "放克音樂", "金典音樂"]
#     super_title_name = ["已發行", "熱門歌曲清單",
#                         "好聽的華語抒情歌", "K-RISING",  "J-Hits!", "放克流行金曲", "00 年代琅琅上口的歌曲", ]
#     super_list = []

#     for name, title in zip(super_title_name, show_title):
#         # obj = Style.objects.filter(style_name=name).first()

#         DiscoverTitle.objects.create(name=name, show_title=title)

#     return Response({"message": "sdsds"})


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='GET'), name='get')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='POST'), name='post')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='PUT'), name='put')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='DELETE'), name='delete')
class DiscoverEditView(APIView):

    def get(self, request):
        discover_table = DiscoverTitleSerializer(
            DiscoverTitle.objects.all(), many=True).data
        return Response({"style_table":  StyleTitle.objects.all().values(), "discover_table": discover_table})

    def put(self, request):
        # if request.data["id1"]:
        #     try:
        #         change_id(request=request)
        #         return Response({"message": "Data swapped and saved successfully"})

        #     except KeyError as e:
        #         return Response({"message": f"KeyError: {str(e)}"}, status=404)
        #     except StopIteration:
        #         return Response({"message": "One or both IDs not found in data"}, status=404)

        serializer = DiscoverTitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully"}, status=201)
        else:
            return Response(serializer.errors, status=404)

    def post(self, request):
        serializer = DiscoverTitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully"}, status=201)
        else:
            return Response(serializer.errors, status=404)

    def delete(self, request):
        try:
            DiscoverTitle.objects.filter(name=request.GET["name"]).delete()
            return Response({"message": "Data saved successfully"}, status=201)
        except Exception as e:
            return Response({"message": str(e)}, status=201)


def change_id(request):
    id1 = request.data["id1"]
    id2 = request.data["id2"]

    DiscoverTitle.objects.filter(id=id2) .update(id=1000)
    # change id
    DiscoverTitle.objects.filter(id=id1) .update(id=id2)
    DiscoverTitle.objects.filter(id=1000) .update(id=id1)
