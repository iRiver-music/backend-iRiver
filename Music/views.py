from django.http import JsonResponse
import json

import difflib

import concurrent.futures


# import sql相關
import Music.sql.config

#import query function
from Music.query import query as query_music

#import models
from .models import Music
from .models import Artist

#import serializers
from .serializers import MusicSerializer
from .serializers import ArtistSerializer

#import clean_str
from Music.clean_str import clear_str

#import user_view
import User.views as user_views

from Music.web_scutter.youtube import query_youtube

#test value
test = False

def get_artist_info(request, artist):
    #artist = request.GET.get('artist')
    #mysql.create_tables()
    r = Artist.objects.using('test').get(artist=artist)
    print('#'*30)
    print(r)
    serializer = ArtistSerializer(r)
    artist_info = serializer.data
    print('artist : ', artist_info)
    if r == "()" or r == None:
        return JsonResponse({'sucess': False})
    return JsonResponse({'musicList': artist_info})


def query_db_song(request, query):
    #query = request.GET.get('query', '')
    if test:
        print('='*50)
        print(f'get db {query} !!')
    # 資料庫
    try:
        #print(query)
        res = query_music(query=query)
        #print(res)
        if res is None:
            print("the res is empty")
            return JsonResponse({'isLogin': False})
    except Exception as e:
        print(f'the res is {e}')
        return JsonResponse({'isLogin': False})

    music_list = []
    #print("asdf", res)
    for row in res:
        serializer = MusicSerializer(row)
        row = serializer.data
        #print('music after serializers : ', row)
        music_list.append(row)

    return JsonResponse({'success': True, 'music_list': music_list}, safe=False)

def query_web_song(request, query):
    #query = request.GET.get('query', '')
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

def query_album(request, be_search_album):
    search_album = Music.objects.using('test').all()
    matches = difflib.get_close_matches(be_search_album, [x.album for x in search_album],n = 6, cutoff=0.06)
    aldum_get = Music.objects.using('test').filter(album__in = matches)
    print('query_album_matches : ', matches)
    album_list = []
    for adbum in aldum_get:
        serializer = MusicSerializer(adbum)
        album_list.append(serializer.data)
    #print(album_list)
    if album_list == []:
        return JsonResponse({'success': False, 'album_list': album_list}, safe=False)
    
    return JsonResponse({'success': True, 'album_list': album_list}, safe=False)


