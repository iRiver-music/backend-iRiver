from .models import Song, StyleTitle
import json
from math import ceil
from .serializers import SongSerializer, StyleTitleSerializer

import os
from django.conf import settings
from django.http import JsonResponse


def make_json_file(request):
    try:
        data = Song.objects.all()
        print('finish get data', data.count())

        file_total = data.count() / 10000 + \
            1 if data.count() % 10000 > 0 else data.count() / 10000
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
                absolute_path = os.path.join(
                    settings.BASE_DIR, 'Music', 'music_db', f'music_db{file_count}.json')
                with open(absolute_path, 'w') as json_file:
                    json_file.write(json_object)
                count = 0
                row = []
                file_count += 1
                print(file_count)
        # Writing to sample.json)

        data = StyleTitle.objects.all()
        print('finish get data', data.count())

        file_total = data.count() / 10000 + \
            1 if data.count() % 10000 > 0 else data.count() / 10000
        print('file_total : ', file_total)
        row = []
        count = 0
        file_count = 0
        for index, i in enumerate(data):
            serializer = StyleTitleSerializer(i)
            row.append(serializer.data)
            count += 1
            if count >= 10000 or index == len(data) - 1:
                input = {'data': row}
                json_object = json.dumps(input, indent=4)
                absolute_path = os.path.join(
                    settings.BASE_DIR, 'Music', 'style_db', f'style_db{file_count}.json')
                with open(absolute_path, 'w') as json_file:
                    json_file.write(json_object)
                count = 0
                row = []
                file_count += 1
                print(file_count)
        return JsonResponse({'make file': True})
    except Exception as e:
        print('Error in  : make_json_file')
        print(e)
        return JsonResponse({'error': str(e)}, status=500)
