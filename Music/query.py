import concurrent.futures
import json
import os
import glob
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


def search_music(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: song_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")

    return results

def search_artist(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: artist_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

def search_album(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: aldum_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

def search_style(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: style_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

def search_artist(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: artist_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

def search_album(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: aldum_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

def search_style(file_name, query) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: style_search(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    

    return results

# 異步

def multiprocess_music(query, music_file_list) -> list :
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(music_file_list)) as executor:
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
    print(type(music_results))
    music_results.append({'who am I ' : 'music'})
    results = music_results[:20]
    results.append(music_results[-1])
    return results


def multiprocess_artist(query, music_file_list) -> list :
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(music_file_list)) as executor:
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
    print(type(artist_results))
    artist_results.append({'who am I ' : 'artist'})
    results = artist_results[:10]
    results.append(artist_results[-1])
    return results

def multiprocess_album(query, music_file_list) -> list :
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(music_file_list)) as executor:
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
    print(type(album_results))
    album_results.append({'who am I ' : 'album'})
    results = album_results[:10]
    results.append(album_results[-1])
    return results

def multiprocess_style(query, music_file_list) -> list :
    manager = Manager()
    search_results = manager.list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(music_file_list)) as executor:
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
    print(type(album_results))
    album_results.append({'who am I ' : 'style'})
    results = album_results[:10]
    results.append(album_results[-1])
    return results


def query(query):
    # manager = Manager()
    # search_results = manager.list()
    try:
        music_file_list = count_music_file()
        style_file_list = count_style_file()
        print('music_file_list : ', len(music_file_list))
        print('music_file_list : ', len(style_file_list))

        # music_results = mutiprocess_music(query, music_file_list)
        music_results = []
        artist_results = []
        album_results = []
        style_results = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor : 
            future_to_music = [executor.submit(multiprocess_music, query, music_file_list)
                                , executor.submit(multiprocess_artist, query, music_file_list)
                                , executor.submit(multiprocess_album, query, music_file_list)
                                , executor.submit(multiprocess_style, query, style_file_list)]

            for future in concurrent.futures.as_completed(future_to_music):
                result = future.result()
                if result[-1]['who am I '] == 'music' : 
                    music_results.extend(result)
                elif result[-1]['who am I '] == 'artist' : 
                    artist_results.extend(result)
                elif result[-1]['who am I '] == 'album' : 
                    album_results.extend(result)
                elif result[-1]['who am I '] == 'style' : 
                    style_results.extend(result)

        data = {
            'song' : music_results, 
            'artist' : artist_results, 
            'album' : album_results, 
            'style' : style_results, 
        }
        print('finish second sort')
    except Exception as e:
        print('Error in new_query : ')
        print(e)
        return {'error in query': str(e)}

    return data
