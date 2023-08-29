import concurrent.futures
import json
import os
import glob
import ijson
from fuzzywuzzy import fuzz
from django.conf import settings
from django.http import JsonResponse

from multiprocessing import Manager

from multiprocessing import Process, Manager


def count_music_file() -> list:
    absolute_path = os.path.join(
        settings.BASE_DIR, 'Music', 'music_db', '*.json')
    json_files = glob.glob(absolute_path)

    return json_files


def count_style_file() -> list:
    absolute_path = os.path.join(
        settings.BASE_DIR, 'Music', 'style_db', '*.json')
    json_files = glob.glob(absolute_path)

    return json_files


def song_search(song, query):
    return fuzz.ratio(query, song['title'])


def artist_search(artist, query):
    return fuzz.ratio(query, artist['artist'])


def aldum_search(aldum, query):
    return fuzz.ratio(query, aldum['album'])


def style_search(style, query):
    return fuzz.ratio(query, style['style']) + fuzz.ratio(query, style['title'])


def read_file(file_name) : 
    results = []
    current_dict = {}
    keys_to_extract = ['title', 'artist', 'album', 'music_ID']
    with open(file_name, 'rb') as file :
        parser = ijson.parse(file)
        in_data_array = False
        for prefix, event, value in parser :
            if in_data_array:
                if event == 'map_key' :
                    current_key = value
                elif event == 'string' and current_key in keys_to_extract :
                    current_dict[current_key] = value
                    if len(current_dict) == len(keys_to_extract):
                        results.append(current_dict)
                        current_dict = {}
            elif prefix == 'data' and event == 'start_array' :
                in_data_array = True
            elif prefix == 'data' and event == 'end_array' :
                in_data_array = False
                break
    return results

def search_music(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    song_list = read_file(file_name)

    results = sorted(song_list, key=lambda song: song_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_artist(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: artist_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_album(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: aldum_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_style(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: style_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_artist(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: artist_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_album(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: aldum_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results


def search_style(file_name, query) -> list:

    # open json file
    # with open(file_name, 'r') as jsonFile:
    #     song_json = json.load(jsonFile)

    # song_list = song_json['data']

    song_list = read_file(file_name)

    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: style_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    # push music_list into the querylist

    return results

# 異步


def multiprocess_music(query, music_file_list) -> list:
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(music_file_list)) as executor:
        future_to_file = {executor.submit(
            search_music, file, query): file for file in music_file_list}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                search_results.extend(result)
            except Exception as exc:
                print(f'An error occurred for file {file}: {exc}')

    music_results = sorted(search_results,  key=lambda song: song_search(
        song, query), reverse=True)
    music_results.append({'who am I ': 'music'})
    results = music_results[:20]
    results.append(music_results[-1])
    return results


def multiprocess_artist(query, music_file_list) -> list:
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(music_file_list)) as executor:
        future_to_file = {executor.submit(
            search_artist, file, query): file for file in music_file_list}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                search_results.extend(result)
            except Exception as exc:
                print(f'An error occurred for file {file}: {exc}')

    artist_results = sorted(search_results,  key=lambda song: artist_search(
        song, query), reverse=True)
    artist_results.append({'who am I ': 'artist'})
    results = artist_results[:10]
    results.append(artist_results[-1])
    return results


def multiprocess_album(query, music_file_list) -> list:
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(music_file_list)) as executor:
        future_to_file = {executor.submit(
            search_album, file, query): file for file in music_file_list}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                search_results.extend(result)
            except Exception as exc:
                print(f'An error occurred for file {file}: {exc}')

    album_results = sorted(search_results,  key=lambda song: aldum_search(
        song, query), reverse=True)
    album_results.append({'who am I ': 'album'})
    results = album_results[:10]
    results.append(album_results[-1])
    return results


def multiprocess_style(query, music_file_list) -> list:
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(music_file_list)) as executor:
        future_to_file = {executor.submit(
            search_style, file, query): file for file in music_file_list}
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                search_results.extend(result)
            except Exception as exc:
                print(f'An error occurred for file {file}: {exc}')

    album_results = sorted(search_results,  key=lambda song: style_search(
        song, query), reverse=True)
    album_results.append({'who am I ': 'style'})
    results = album_results[:10]
    results.append(album_results[-1])
    return results


def query(query):
    # manager = Manager()
    # search_results = manager.list()
    try :
        music_file_list = count_music_file()
        style_file_list = count_style_file()

        # music_results = mutiprocess_music(query, music_file_list)
        music_results = []
        artist_results = []
        album_results = []
        style_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
            future_music = executor.submit(
                multiprocess_music, query, music_file_list)
            future_artist = executor.submit(
                multiprocess_artist, query, music_file_list)
            future_album = executor.submit(
                multiprocess_album, query, music_file_list)
            future_style = executor.submit(
                multiprocess_style, query, style_file_list)

            # 使用as_completed等待所有任务完成
            for future in concurrent.futures.as_completed([future_music, future_artist, future_album, future_style]):
                result = future.result()
                if result[-1]['who am I '] == 'music':
                    music_results.extend(result)
                elif result[-1]['who am I '] == 'artist':
                    artist_results.extend(result)
                elif result[-1]['who am I '] == 'album':
                    album_results.extend(result)
                elif result[-1]['who am I '] == 'style':
                    style_results.extend(result)

        del music_results[-1]
        del artist_results[-1]
        del album_results[-1]
        del style_results[-1]

        # 將每個陣列的前五筆資料取平均分數，將分數最大的項回傳，告訴前端此項優先顯示。
        # 測試演算法分數，設定一個閾值，如果分數最大項與分數第二大項平均分數相差超過閾值，則做關聯性比較（例：如果查詢稻香，
        # song的分數比artist高出閾值，則將song第一項對應的aritst項（周杰倫）推進artist list的第一項，style不用做）。
        # 現在是將每項的19筆資料存進來，有內存隱患，改為將每項的4筆資料傳進來，分別為title, artist, album, ID。

        data = {
            'song' : music_results,
            'artist' : artist_results,
            'album' : album_results,
            'style' : style_results,
        }

        

        print('finish second sort')
    except Exception as e:
        return {'error in query': str(e)}

    return data
