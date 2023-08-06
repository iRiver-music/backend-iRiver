import MySQLdb
import json
import difflib
from fuzzywuzzy import fuzz, process

from .models import Song
from .models import Artist
from .serializers import ArtistSerializer
from .serializers import SongSerializer


def query(query):
    artist_song_res, artist_song_sorce = query_all_artist_song(
        artist=query) or (None, 0)
    song_res, song_score = query_song(song_name=query) or (None, 0)
    # print(artist_song_res, artist_song_sorce)
    # print(song_res, song_score)

    if (artist_song_sorce > song_score):
        forwards = artist_song_res
        back = song_res
    else:
        forwards = song_res
        back = artist_song_res

    result = []
    if forwards is not None:
        result.extend(forwards)
    if back is not None:
        result.extend(back)
    # print('result : ', result)
    return result


def query_all_artist_song(artist):
    # r =self.get_all_artist()
    r = list(Artist.objects.all())
    # print(r)

    try:
        # print('inside')
        matches = difflib.get_close_matches(
            artist, [x['artist'] for x in r], n=3, cutoff=0.4)

        print("query_all_artist_song matches:", matches)
        score = difflib.SequenceMatcher(None, artist, matches[0]).ratio()
        # print("score:", score)
    except Exception as e:
        print("ERROR in query_all_artist_song at query.py")
        print(e)
        return None, 0
    if matches is None:
        print('match is none')
        return None, 0
    result = Song.objects.filter(
        artist__in=matches).order_by('-views')[:4]
    # print("result:", result)
    # result -> QureySet
    return result, score


def query_song(song_name):
    # r = self.get_all_song(field='title')
    r = list(Song.objects.values(
        'title').all().order_by('-views'))
    # print('music:', r)

    try:
        matches = difflib.get_close_matches(
            song_name, [x['title'] for x in r], n=3, cutoff=0.0003)
        print("query_song matches", matches)
        score = difflib.SequenceMatcher(None, song_name, matches[0]).ratio()
        # print('*'*20)
        # print(f'get_song sorce{score}')
    except Exception as e:
        print("ERROR in query_song at query.py")
        print(e)
        return None, 0
    if not matches:
        return None, 0
    result = Song.objects.filter(
        title__in=matches).order_by('-views')[:4]
    # print('query_song : ', result)
    # print('query_song : ', score)
    return result, score

def new_query_song(song_name) : 
    end_query_list = []
    # 迴圈開啟1~10的json檔
    for i in range(10) : 
        # 開啟
        jsonFile = open(f'music_db.music_db{i}.json', 'w')
        # 將json轉成dict
        song_json = json.load(jsonFile)
        # 將json中的音樂陣列取出來
        song_list = song_json['data']
        # 使用fuzzywuzzy 中的ratio 演算法對陣列中的每一個音樂做相似度評分及大到小排序
        results = process.extract(song_name, song_list['title'], limit=20, scorer=fuzz.ratio)
        # 將評分並排序完的music list 推入list中
        end_query_list.append(results)
    return end_query_list