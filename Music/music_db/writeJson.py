from ..models import Song
import json
from math import ceil
from ..serializers import SongSerializer

import os
from django.conf import settings
from django.http import JsonResponse


def jsonTest(request):
    try : 
        a = Song.objects.all()
        row = []
        count = 0
        for i in a : 
            serializer = SongSerializer(i)
            row.append(serializer.data)
            count += 1
            if count >= 100 : 
                break

        print('finished')
        win = {'data': row}
        print('win')
        json_ob = json.dumps(win, indent=4)
        absolute_path = os.path.join(settings.BASE_DIR, 'Music', 'music_db',f'music_db0.json')
        with open(absolute_path, "w") as json_file:
            json_file.write(json_ob)
        print('finish write')
        print(type(row))
        print(row)
        return JsonResponse(win)
    except Exception as e:
        print('Error in  : make_json_file')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)


def cutjson():
    all = Song.objects.using('test').all()
    total_records = all.count()
    chunk_size = ceil(total_records / 10)  # 使用ceil確保每份資料不會有缺漏
# 將資料分成10份
    data_chunks = [all[i:i + chunk_size]
                   for i in range(0, total_records, chunk_size)]
    data_array = []
    count = 0
    for data_list in data_chunks:
        for row in data_list:
            serializer = SongSerializer(row)
            row = serializer.data
            # print('music after serializers : ', row)
            data_array.append(row)

        jsonFile = open(f'music_db{count}.json', 'w')
        beWrite = {'data': data_array}
        json.dump(beWrite, jsonFile)
        count += 1

def make_json_file(request):
    try : 
        data = Song.objects.all()
        print('finish get data')
        file_total = data.count() / 10000 + 1 if data.count() % 10000 > 0 else data.count() / 10000
        print('file_total : ', file_total)
        row = []
        count = 0
        file_count = 0
        for index, i in enumerate(data): 
            serializer = SongSerializer(i)
            row.append(serializer.data)
            count += 1
            if count >= 10000 or index == len(data) - 1: 
                input = {'data': row}
                json_object = json.dumps(input, indent=4)
                absolute_path = os.path.join(settings.BASE_DIR, 'Music', 'music_db',f'music_db{file_count}.json')
                with open(absolute_path, 'w') as json_file:
                    json_file.write(json_object)
                count = 0
                row = []
                file_count += 1
                print(file_count)
        # Writing to sample.json)
        return JsonResponse({'make file' : True})
    except Exception as e:
        print('Error in  : make_json_file')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)
        
