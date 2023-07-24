from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
import requests
import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
import threading
import re
from urllib.parse import unquote
from multiprocessing import Process, Queue
import concurrent.futures
from django.urls import reverse
from django.shortcuts import redirect
# 自製 : 

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
from Music.web_scutter.iocn import query_artist_iocn_src
from Music.web_scutter.summary import query_summary
from Music.web_scutter.music_list import query_music_list
from Music.web_scutter.music_ID_info import get_music_ID_info

#test value
test = False

# Create your views here.


# def music_list(request):
#     artist = request.GET.get('artist', '')
#     index = request.GET.get('index', '')
#     music_list_infos = Music.objects.using('test').filter(artist=artist).values().order_by('-views')
#     summary_str = Artist.objects.get(artist=artist).value('summary')
#     summary = "".join(item[0] for item in summary_str)

#     response_data = {
#         'artist': artist,
#         'index': index,
#         'music_list_infos': music_list_infos,
#         'summary': summary,
#     }

#     return JsonResponse(response_data)

# def get_my_music_list(request):

#     music_list = request.GET.get('music_list', "我的最愛 ")
#     # 解析请求体数据为字典
#     try:
#         request_body = json.loads(request.body.decode('utf-8'))
#     except json.JSONDecodeError:
#         request_body = {}

#     # 添加两个键值对到请求体的字典中
#     request_body['method'] = 'get'
#     request_body['music_list'] = music_list

#     # 将更新后的字典重新编码为JSON字符串
#     updated_body = json.dumps(request_body)

#     # 将更新后的请求体数据重新设置回请求对象
#     request._body = updated_body.encode('utf-8')

#     # 调用目标视图函数并传递请求对象及其他参数
#     response = user_views.get_user_music_list(request=request)

#     # url = 'http://127.0.0.1:8000/u ser/get_user_music_list/'
#     # csrftoken = request.COOKIES.get('csrftoken')
#     # session_id = request.COOKIES.get('sessionid')
#     # headers = {'Cookie': f'csrftoken={csrftoken}; sessionid={session_id};'}
#     # data = {'method': 'get', "playlist": music_list}
#     # headers['X-CSRFToken'] = csrftoken
#     # response = requests.post(url, headers=headers, data=json.dumps(data))

#     music_ID_list=[item[0] for item in json.loads(response.content)]
#     music_list_infos = []
#     for music_id in music_ID_list :
#         music_info = Music.objects.using('test').get(music_ID=music_id)
#         music_list_infos.append()
    
#     response_data = {
#         'music_list_infos': music_list_infos,
#         'music_list': music_list,
#     }

#     return JsonResponse(response_data)

def get_artist_music_list(request):
    artist = request.GET.get('artist')
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


def query_db_song(request):
    query = request.GET.get('query', '')
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

def query_web_song(request):
    query = request.GET.get('query', '')
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



