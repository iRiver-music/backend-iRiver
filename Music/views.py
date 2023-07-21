from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
import requests
import json
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Music
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
from Music.sql.sql import SQL

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


def search(request):
    query = request.GET.get('query', '')
    context = {'query': query}

    return JsonResponse(context)



def music_list(request):
    artist = request.GET.get('artist', '')
    index = request.GET.get('index', '')
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    music_list_infos = mysql.get_all_artist_song(artist=artist)
    summary_str = mysql.get_artist_summary(artist=artist)
    summary = "".join(item[0] for item in summary_str)

    response_data = {
        'artist': artist,
        'index': index,
        'music_list_infos': music_list_infos,
        'summary': summary,
    }

    return JsonResponse(response_data)

def get_my_music_list(request):

    music_list = request.GET.get('music_list', "我的最愛 ")
    # 解析请求体数据为字典
    try:
        request_body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        request_body = {}

    # 添加两个键值对到请求体的字典中
    request_body['method'] = 'get'
    request_body['music_list'] = music_list

    # 将更新后的字典重新编码为JSON字符串
    updated_body = json.dumps(request_body)

    # 将更新后的请求体数据重新设置回请求对象
    request._body = updated_body.encode('utf-8')

    # 调用目标视图函数并传递请求对象及其他参数
    response = user_views.get_user_music_list(request=request)

    # url = 'http://127.0.0.1:8000/u ser/get_user_music_list/'
    # csrftoken = request.COOKIES.get('csrftoken')
    # session_id = request.COOKIES.get('sessionid')
    # headers = {'Cookie': f'csrftoken={csrftoken}; sessionid={session_id};'}
    # data = {'method': 'get', "playlist": music_list}
    # headers['X-CSRFToken'] = csrftoken
    # response = requests.post(url, headers=headers, data=json.dumps(data))

    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    music_list_infos = mysql.get_music_list_infos(
        music_ID_list=[item[0] for item in json.loads(response.content)])
    try:
        title_img_url = f"/media/{music_list_infos[0]['artist']}/img/{music_list_infos[0]['music_ID']}.jpg"
    except:
        title_img_url = "/static/img/music_img.jpg"
    
    response_data = {
        'music_list_infos': music_list_infos,
        'music_list': music_list,
        'title_img_url': title_img_url,
    }

    return JsonResponse(response_data)

def get_music_list(request):
    artist = request.GET.get('artist')
    mysql = SQL(music.lib.sql.config.DB_CONFIG)
    mysql.create_tables()
    r = mysql.get_all_artist_song(artist=artist)
    print('#'*30)
    print(r)

    result_list = []
    if r == "()":
        return JsonResponse({'sucess': False})

    for row in r:
        result_list.append(row)

    return JsonResponse({'musicList': result_list})

def query_db_song(request):
    query = request.GET.get('query', '')
    if test:
        print('='*50)
        print(f'get db {query} !!')
    # 資料庫
    try:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        res = mysql.query(query=query)
        if res is None:
            print("the res is empty")
            return JsonResponse({'isLogin': False})
    except Exception as e:
        print(f'the res is {e}')
        return JsonResponse({'isLogin': False})

    music_list = []
    for row in res:
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

def is_song_exist(request):
    music_ID = request.get('music_ID', None)
    if music_ID:
        mysql = SQL(music.lib.sql.config.DB_CONFIG)
        # mysql.query_song()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})



