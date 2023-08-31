import MySQLdb
import json
import difflib
import os
import glob
import concurrent.futures

from fuzzywuzzy import fuzz, process
from django.conf import settings
from django.http import JsonResponse

from .models import Song
from .models import Artist
from .serializers import ArtistSerializer
from .serializers import SongSerializer

from multiprocessing import Process, Manager


def count_file() -> list:
    absolute_path = os.path.join(
        settings.BASE_DIR, 'Music', 'music_db', '*.json')
    json_files = glob.glob(absolute_path)

    return json_files


def song_search(song, query):
    return fuzz.ratio(query, song['title'])


def search_music(file_name, query, results_list) -> list:

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
    # push music_list into the querylist
    print("finish sorted")
    results_list.append(results)


def new_query(request, query):
    processes = []
    manager = Manager()
    first_results = manager.list()
    try:
        file_list = count_file()
        print('file_list : ', file_list)
        # search_music(file_list[0], query, processes)
        # print(processes)
        for file in file_list:
            p = Process(target=search_music, args=(file, query, first_results))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
        search_list = []
        for result_list in first_results:
            for i in result_list:
                search_list.append(i)

        results = sorted(search_list, key=lambda song: song_search(
            song, query), reverse=True)
        print('finish second sort')
    except Exception as e:
        print('Error in new_query : ')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'data': results})
