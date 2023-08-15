from django.http import JsonResponse
import json

import difflib

import concurrent.futures


# import sql相關
# import query function
from Music.query import query as query_music

# import models
from .models import Song, Artist, Style

# import serializers
from .serializers import ArtistSerializer, SongSerializer, StyleSerializer

# import clean_str
from Music.clean_str import clear_str

# # import user_view
# import User.views as user_views

from Music.web_scutter.youtube import query_youtube


# 異步版本

from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async

# rest_framework
from rest_framework import generics
from rest_framework.response import Response

test = False


@api_view(['GET'])
def query_db_song(request, query):
    # 資料庫
    try:
        # print(query)
        res = query_music(query=query)
        # print(res)
        if res is None:
            print("the res is empty")
            return JsonResponse({'isLogin': False})
    except Exception as e:
        print(f'the res is {e}')
        return JsonResponse({'isLogin': False})

    music_list = []
    # print("asdf", res)
    for row in res:
        serializer = SongSerializer(row)
        row = serializer.data
        # print('music after serializers : ', row)
        music_list.append(row)

    data = {
        "song": [],
        "artist": [],
        "album": [],
        "style": [],
    }

    return JsonResponse(data=data)


@api_view(['GET'])
def query_web_song(request, query):
    # query = request.GET.get('query', '')
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_youtube = executor.submit(query_youtube, query)
    # 網路
    if test:
        print('='*50)
        print(f'get  {query}  !!')
    try:
        youtube_result = json.loads(future_youtube.result())
        music_list = youtube_result['music_list']
        statistics = youtube_result['statistics']
    except Exception as e:
        print(e)
    return JsonResponse({'success': True, 'music_list': music_list}, safe=False)


@api_view(['GET'])
def album(request, album):
    search_album = Music.objects.all()
    matches = difflib.get_close_matches(
        album, [x.album for x in search_album], n=6, cutoff=0.06)
    aldum_get = Music.objects.filter(album__in=matches)
    print('query_album_matches : ', matches)
    album_list = []
    for adbum in aldum_get:
        serializer = Song(adbum)
        album_list.append(serializer.data)
    # print(album_list)
    if album_list == []:
        return JsonResponse({'success': False, 'album_list': album_list}, safe=False)

    return JsonResponse({'success': True, 'album_list': album_list}, safe=False)

# 49.213.238.75:5001


@api_view(['GET'])
def songs(request, artist):
    songs_data = Song.objects.filter(
        artist=artist).values().order_by('-views')

    return Response(songs_data)


@api_view(['GET'])
def artist(request, artist):
    songs_data = Song.objects.filter(
        artist=artist).values().order_by('-views')

    artist_data = ArtistSerializer(Artist.objects.filter(
        artist=artist).values(), many=True).data

    response_data = {
        'id': 1,
        'artist': artist_data,
        'songs': songs_data
    }
    return Response(response_data)


# style =================================================================


@api_view(['GET'])
def style(request, style):
    obj = Style.objects.filter(style=style)

    if obj.exists():
        serializer = StyleSerializer(obj, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Style not found"}, status=404)


# test ==============================================


@api_view(['GET'])
def artist_test(request, artist):
    songs_data = Song.objects.filter(
        artist=artist).values().order_by('-views')
    artist_data = ArtistSerializer(Artist.objects.filter(
        artist=artist).values(), many=True).data

    response_data = {
        'id': 1,
        'artist': artist_data,
        'songs': songs_data
    }
    return Response(response_data)
