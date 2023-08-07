from ..models import Song
import json
from math import ceil
from ..serializers import SongSerializer


def jsonTest():
    a = Song.objects.using('test').all()
    jsonFile = open('music_db0.json', 'w')
    win = {'data': a}
    json.dump(win, jsonFile)
    print('win : ')
    print(win)


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
