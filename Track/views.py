import datetime
from .models import Artist, ArtistViewsCount
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from django.http import HttpRequest
from rest_framework.response import Response

# models
# rest_framework
from rest_framework.decorators import api_view, authentication_classes
from Music.models import Song, Artist

from Track.models import DailyViews, MusicViews, RegisterViews, SongViewsCount, ArtistViewsCount,  FavSongViewsCount, Tab, TabViews, UserDevice, SearchViews
from django_user_agents.utils import get_user_agent

from lib.Email.send import send_style_mail


@api_view(['GET'])
def init(request):
    try:
        tab_list = ["discoverer", "myPlaylist", "myData", "search", "user"]

        for tab in tab_list:
            if not Tab.objects.filter(tab=tab).exists():
                Tab.objects.create(tab=tab)

        # create data
        views_request = HttpRequest()
        views_request.method = 'GET'

        views(request=views_request)
        music_view(request=views_request)
        search_view(request=views_request)
        # artist
        views_request.GET = {"artist": "PMalone"}
        artist_view(request=views_request)
        # song
        views_request.GET = {"music_ID": "YbU5y5iIY7M"}
        song_view(request=views_request)
        # fav
        fav_view(request=views_request)

        # tab
        views_request.GET = {"tab": "myPlaylist"}
        tab_view(request=views_request)

        # register_views
        register_views(request=views_request)

        return Response({"message": "Initialization successful"})
    except Exception as e:
        # 如果发生错误，返回错误响应
        return Response({"message": str(e)}, status=500)


# DailyViews =============================================================


@api_view(['GET'])
def views(request):
    # 获取今天的日期
    today = date.today()

    # 尝试获取今天的瀏覽次數记录，如果不存在则创建
    daily_views, created = DailyViews.objects.get_or_create(
        date=today, defaults={'views_count': 0})

    # 增加瀏覽次數
    daily_views.views_count += 1
    daily_views.save()

    return Response({"date": today, "views_count": daily_views.views_count})

# music_View =============================================================


@api_view(['GET'])
def music_view(request):
    # 获取今天的日期
    today = date.today()

    # 尝试获取今天的瀏覽次數记录，如果不存在则创建
    daily_views, created = MusicViews.objects.get_or_create(
        date=today, defaults={'views_count': 0})

    # 增加瀏覽次數
    daily_views.views_count += 1
    daily_views.save()

    return Response({"date": today, "views_count": daily_views.views_count})


# search_View =============================================================


@api_view(['GET'])
def search_view(request):
    # 获取今天的日期
    today = date.today()

    # 尝试获取今天的瀏覽次數记录，如果不存在则创建
    daily_views, created = SearchViews.objects.get_or_create(
        date=today, defaults={'views_count': 0})

    # 增加瀏覽次數
    daily_views.views_count += 1
    daily_views.save()

    return Response({"date": today, "views_count": daily_views.views_count})


# artist view =================================================================


@api_view(['GET'])
def artist_view(request):
    try:
        # 从请求中获取艺术家的名称
        artist_name = request.GET.get('artist')  # 从查询参数中获取艺术家名称

        # 获取与艺术家名称相匹配的艺术家对象
        artist_obj = get_object_or_404(Artist, artist=artist_name)

        # 获取艺术家在今天的点击次数记录，如果不存在则创建
        # 注意：你可以根据需要修改日期逻辑
        artist_views, created = ArtistViewsCount.objects.get_or_create(
            artist=artist_obj,
        )

        # 增加点击次数
        artist_views.views_count += 1
        artist_views.save()

        return Response({"ok": True})
    except Artist.DoesNotExist:
        return Response({"message": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)


# song view =======================================================


@api_view(['GET'])
def song_view(request):
    try:
        # 从请求中获取歌曲的ID
        music_ID = request.GET.get('music_ID')  # 从查询参数中获取歌曲ID

        # 获取与 song_id 相关的歌曲对象
        song = Song.objects.get(music_ID=music_ID)

        # 尝试获取歌曲的瀏覽次數记录，如果不存在则创建
        song_views, created = SongViewsCount.objects.get_or_create(song=song)

        # 增加瀏覽次數
        song_views.views_count += 1
        song_views.save()

        return Response({"ok": True})
    except Song.DoesNotExist:
        return Response({"message": "Song not found"}, status=404)

# fav views =================================================================


@api_view(['GET'])
def fav_view(request):
    try:
        # 从请求中获取歌曲的ID
        music_ID = request.GET.get('music_ID')  # 从查询参数中获取歌曲ID

        # 获取与 song_id 相关的歌曲对象
        song = Song.objects.get(music_ID=music_ID)

        # 尝试获取歌曲的瀏覽次數记录，如果不存在则创建
        song_views, created = FavSongViewsCount.objects.get_or_create(
            song=song)

        # 增加瀏覽次數
        song_views.views_count += 1
        song_views.save()

        return Response({"ok": True})
    except Song.DoesNotExist:
        return Response({"message": "Song not found"}, status=404)


# Tab views  =================================================


@api_view(['GET'])
def tab_view(request):
    try:
        tab = request.GET.get('tab')  # 从查询参数中获取歌曲ID

        # 获取与 song_id 相关的歌曲对象
        tab_obj = Tab.objects.get(tab=tab)

        # 尝试获取歌曲的瀏覽次數记录，如果不存在则创建
        tab_views, created = TabViews.objects.get_or_create(tab=tab_obj)

        # 增加瀏覽次數
        tab_views.views_count += 1
        tab_views.save()

        return Response({"ok": True})
    except Song.DoesNotExist:
        return Response({"message": "Tab not found"}, status=404)


# Device views  =======================================================================================


@api_view(['GET'])
def device_view(request):

    device = get_user_agent(request)

    if device.is_mobile:
        device = "mobile"
    elif device.is_tablet:
        device = "tablet"
    elif device.is_touch_capable:
        device = "touch_capable"
    elif device.is_pc:
        device = "pc"
    elif device.is_bot:
        device = "bot"

    try:
        # 尝试获取歌曲的瀏覽次數记录，如果不存在则创建
        device_views, created = UserDevice.objects.get_or_create(device=device)

        # 增加瀏覽次數
        device_views.count += 1
        device_views.save()

        return Response({"ok": True})
    except UserDevice.DoesNotExist:
        return Response({"message": "TabViews not found"}, status=404)


# daily registration views =================================================================================

@api_view(['GET'])
def register_views(request):
    # 获取今天的日期
    today = date.today()

    # 尝试获取今天的瀏覽次數记录，如果不存在则创建
    daily_reg_views, created = RegisterViews.objects.get_or_create(
        date=today, defaults={'views_count': 0})

    # 增加瀏覽次數
    daily_reg_views.views_count += 1
    daily_reg_views.save()

    return Response({"date": today, "views_count": daily_reg_views.views_count})


@api_view(['GET'])
def test(request):
    device = get_user_agent(request)

    if device.is_mobile:
        device = "mobile"
    elif device.is_tablet:
        device = "tablet"
    elif device.is_touch_capable:
        device = "touch_capable"
    elif device.is_pc:
        device = "pc"
    elif device.is_bot:
        device = "bot"

    return Response({"ok": device})
