# 多線程
import concurrent.futures
# 異步版本
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Music.models import Artist, DowARtist, Song
from rest_framework.response import Response
from Track.models import ArtistViewsCount, DailyViews, FavSongViewsCount, MusicViews, RegisterViews, SearchViews, SongViewsCount, TabViews, UserDevice

from User.Authentication.authentication import HasLevelFivePermission
from User.models import Profile

# Create your views here.


@permission_classes([HasLevelFivePermission])
@api_view(['GET'])
def info(request):
    try:

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 使用 submit() 方法提交要执行的函数
            # info
            future_info_views = executor.submit(get_info)

            future_dailyViews = executor.submit(get_dailyViews)
            future_searchViews = executor.submit(get_searchViews)
            future_musicViews = executor.submit(get_musicViews)
            future_rgisterViews = executor.submit(get_rgisterViews)
            # 圓餅圖
            future_get_user_device = executor.submit(get_user_device)

            future_song_views = executor.submit(get_song)
            future_artist_views = executor.submit(get_artist)
            future_fav_song_views = executor.submit(get_fav_song)
            future_tab_views = executor.submit(get_tab)

        # 获取结果

        info = future_info_views.result()

        daily_views_dict = future_dailyViews.result()
        search_views_dict = future_searchViews.result()
        music_views_dict = future_musicViews.result()
        register_views_dict = future_rgisterViews.result()

        # 圓餅圖
        user_device = future_get_user_device.result()

        # 折線圖
        artist_views = future_artist_views.result()
        song_views = future_song_views.result()
        fav_song_views = future_fav_song_views.result()
        tab_views = future_tab_views.result()

        return Response({
            # static data
            "song_c": info["song_c"],
            "artist_c": info["artist_c"],
            "user_c": info["user_c"],
            'dow_c':  info["dow_c"],
            # views
            "daily_views": daily_views_dict,
            "search_views":  search_views_dict,
            "music_views": music_views_dict,
            "register_views": register_views_dict,

            # 圓餅圖
            "user_device": user_device,
            # 折線圖
            "song_views": song_views,
            "artist_views":  artist_views,
            "fav_song_views": fav_song_views,
            "tab_views": tab_views,
        })
    except Exception as e:
        return Response({"mes": str(e)}, status=404)


def get_info():
    song_c = Song.objects.all().count()
    artist_c = Artist.objects.all().count()
    user_c = Profile.objects.all().count()
    dow_c = DowARtist.objects.all().count()

    return {"song_c": song_c,
            "artist_c": artist_c,
            "user_c": user_c,
            'dow_c': dow_c}


def get_dailyViews():
    daily_views_obj = DailyViews.objects.all()

    views_count_list = list(
        daily_views_obj.values_list("views_count", flat=True))
    date_list = list(daily_views_obj.values_list("date", flat=True))

    return {
        "views_count": views_count_list,
        "date": date_list
    }


def get_searchViews():
    search_views_obj = SearchViews.objects.all()
    return {
        "views_count": list(search_views_obj.values_list("views_count", flat=True)),
        "date": list(search_views_obj.values_list("date", flat=True))
    }


def get_musicViews():
    music_views_obj = MusicViews.objects.all()
    return {
        "views_count": list(music_views_obj.values_list("views_count", flat=True)),
        "date": list(music_views_obj.values_list("date", flat=True))
    }


def get_rgisterViews():
    register_views_objs = RegisterViews.objects.all()
    return {
        "views_count": list(register_views_objs.values_list("views_count", flat=True)),
        "date": list(register_views_objs.values_list("date", flat=True))
    }


def get_song():
    song_views_objects = SongViewsCount.objects.all().order_by(
        "-views_count")[:5]

    # 创建一个空字典
    song_views_list = []

    # 遍历查询集并将歌曲标题和点击次数添加到字典中
    for song_views_obj in song_views_objects:
        song_views_dict = {}
        song = song_views_obj.song
        song_title = song.title
        views_count = song_views_obj.views_count

        song_views_dict["title"] = song_title
        song_views_dict["views_count"] = views_count

        song_views_list.append(song_views_dict)

    return song_views_list


def get_artist():
    artist_views_objects = ArtistViewsCount.objects.all().order_by(
        "-views_count")[:5]

    # 创建一个空字典
    artist_views_list = []

    # 遍历查询集并将歌曲标题和点击次数添加到字典中
    for artist_views_obj in artist_views_objects:
        artist_views_dict = {}

        artist = artist_views_obj.artist

        artist_title = artist.artist
        views_count = artist_views_obj.views_count

        artist_views_dict["title"] = artist_title
        artist_views_dict["views_count"] = views_count

        artist_views_list.append(artist_views_dict)

    return artist_views_list


def get_fav_song():
    song_views_objects = FavSongViewsCount.objects.all().order_by(
        "-views_count")[:5]

    # 创建一个空字典
    song_views_list = []

    # 遍历查询集并将歌曲标题和点击次数添加到字典中
    for song_views_obj in song_views_objects:
        song_views_dict = {}
        song = song_views_obj.song
        song_title = song.title
        views_count = song_views_obj.views_count

        song_views_dict["title"] = (song_title)
        song_views_dict["views_count"] = (views_count)

        song_views_list.append(song_views_dict)

    return song_views_list


def get_tab():
    tab_views_objects = TabViews.objects.all()

    # 创建一个空字典
    tab_views_list = []

    # 遍历查询集并将歌曲标题和点击次数添加到字典中
    for tab_views_obj in tab_views_objects:
        tab_views_dict = {}
        tab = tab_views_obj.tab
        tab_title = tab.tab
        views_count = tab_views_obj.views_count

        tab_views_dict["title"] = tab_title
        tab_views_dict["views_count"] = views_count

        tab_views_list.append(tab_views_dict)

    return tab_views_list


def get_user_device():
    user_device_objects = UserDevice.objects.all()
    #     if device.is_mobile:
    #     device = "mobile"
    # elif device.is_tablet:
    #     device = "tablet"
    # elif device.is_touch_capable:
    #     device = "touch_capable"
    # elif device.is_pc:
    #     device = "pc"
    # elif device.is_bot:
    #     device = "bot"
    return {
        "mobile": user_device_objects.filter(device='mobile').values_list("count", flat=True).first() or 0,
        "tablet": user_device_objects.filter(device='tablet').values_list("count", flat=True).first() or 0,
        "touch_capable": user_device_objects.filter(device='touch_capable').values_list("count", flat=True).first() or 0,
        "pc": user_device_objects.filter(device='pc').values_list("count", flat=True).first() or 0,
        "bot": user_device_objects.filter(device='bot').values_list("count", flat=True).first() or 0
    }
