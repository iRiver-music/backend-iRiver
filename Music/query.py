import concurrent.futures
import MySQLdb
import json
import difflib
import os
import glob
from fuzzywuzzy import fuzz, process
from django.conf import settings
from django.http import JsonResponse

from .models import Song
from .models import Artist

from multiprocessing import Process, Manager

def count_file() -> list:
    absolute_path = os.path.join(
        settings.BASE_DIR, 'Music', 'music_db', '*.json')
    json_files = glob.glob(absolute_path)

    return json_files


def song_search(song, query):
    return fuzz.ratio(query, song['title'])

def artist_search(artist, query):
    return fuzz.ratio(query, artist['artist'])

def aldum_search(aldum, query):
    return fuzz.ratio(query, aldum['title'])

def style_search(style, query):
    return fuzz.ratio(query, style['style'])


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

# 異步


def new_query(request, query):
    processes = []
    manager = Manager()
    search_results = manager.list()
    try:
        file_list = count_file()
        print('file_list : ', len(file_list))

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(file_list)) as executor:
            future_to_file = {executor.submit(
                search_music, file, query): file for file in file_list}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    search_results.extend(result)
                except Exception as exc:
                    print(f'An error occurred for file {file}: {exc}')

        music_results = sorted(search_results,  key=lambda song: song_search(
                song, query), reverse=True)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(file_list)) as executor:
            future_to_file = {executor.submit(
                search_music, file, query): file for file in file_list}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    search_results.extend(result)
                except Exception as exc:
                    print(f'An error occurred for file {file}: {exc}')

        artist_results = sorted(search_results,  key=lambda song: artist_search(
                song, query), reverse=True)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(file_list)) as executor:
            future_to_file = {executor.submit(
                search_music, file, query): file for file in file_list}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    search_results.extend(result)
                except Exception as exc:
                    print(f'An error occurred for file {file}: {exc}')

        album_results = sorted(search_results,  key=lambda song: aldum_search(
                song, query), reverse=True)

        data = {
            'song' : music_results, 
            'artist' : artist_results, 
            'album' : album_results, 
        }
        print('finish second sort')
    except Exception as e:
        print('Error in new_query : ')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'data': data})
