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

    # print(r)z

    try:
        r = list(Artist.objects.all())
        print('inside')
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


def count_file() -> list:
    absolute_path = os.path.join(
        settings.BASE_DIR, 'Music', 'music_db', '*.json')
    json_files = glob.glob(absolute_path)

    return json_files


def custom_sort(song, query):
    return fuzz.ratio(query, song['title'])


def search_music(file_name, query, results_list) -> list:

    # open json file
    with open(file_name, 'r') as jsonFile:
        song_json = json.load(jsonFile)

    song_list = song_json['data']
    # use radio algorithnm in fuzzywuzzy to sort music by rate (high to low)

    results = sorted(song_list, key=lambda song: custom_sort(
        song, query), reverse=True)
    results = results[:20]
    # print(type(results))
    # print(results)
    print(len(results))
    # push music_list into the querylist
    print("finish sorted")
    results_list.append(results)

    return results_list

# 異步


def new_query(request, query):
    processes = []
    manager = Manager()
    first_results = manager.list()
    try:
        file_list = count_file()
        print('file_list : ', len(file_list))

        # search_music(file_list[0], query, processes)
        # print(processes)
        # for file in file_list:
        #     p = Process(target=search_music, args=(file, query, first_results))
        #     processes.append(p)
        #     p.start()

        # for p in processes:
        #     p.join()

        # search_list = []

        # for result_list in first_results:
        #     for i in result_list:
        #         search_list.append(i)

        search_results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(file_list)) as executor:
            future_to_file = {executor.submit(
                search_music, file, query, first_results): file for file in file_list}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    search_results.extend(result)
                except Exception as exc:
                    print(f'An error occurred for file {file}: {exc}')

        lista = []

        for result_list in first_results:
            for i in result_list:
                lista.append(i)

        print(search_results[0])

        print(type(search_results))

        try:
            results = sorted(lista,  key=lambda song: custom_sort(
                song, query), reverse=True)
        except Exception as e:
            print(e)

        print(len(results))

        print('finish second sort')
    except Exception as e:
        print('Error in new_query : ')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'data': results})
