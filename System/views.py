# from django.shortcuts import render

# # Create your views here.
# import datetime
# import os
# import subprocess
# import time
# from django.http import JsonResponse
# from django.shortcuts import render

# # 異步版本
# from drfa.decorators import api_view
# from asgiref.sync import sync_to_async

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import psutil
# import platform

# import platform
# import cpuinfo
# import GPUtil

# from django.conf import settings

# from User.models import AdminCount, Profile
# from Music.models import Song, StyleTitle, DowARtist, Artist

# from User.serializers import AdminSerializer


# @api_view(['GET'])
# def get(request):
#     # 獲取CPU相關信息

#     cpu_logical_count = psutil.cpu_count(logical=True)
#     cpu_physical_count = psutil.cpu_count(logical=False)
#     cpu_model = platform.processor()

#     # 獲取記憶體型號
#     info = cpuinfo.get_cpu_info()
#     memory_model = info.get('brand_raw', 'N/A')

#     # 獲取GPU型號
#     gpus = GPUtil.getGPUs()
#     gpu_models = [gpu.name for gpu in gpus]

#     mem = psutil.virtual_memory()
#     total_memory = round(mem.total / (1024**3), 2)

#     net_usage = psutil.net_io_counters().bytes_recv / (1024 * 1024)

#     # 將網路用量轉換為 MB 並取小數點後兩位
#     net_usage_mb = round(net_usage, 2)

#     data = {
#         'net_usage_mb': net_usage_mb,
#         'cpu_logical_count': cpu_logical_count,
#         'cpu_physical_count': cpu_physical_count,
#         'cpu_model': cpu_model,
#         'memory_model': memory_model,
#         'total_memory': total_memory,
#         '_memory': psutil.disk_partitions(),
#         'gpu_models': gpu_models,
#     }

#     return Response(data)


# @api_view(['GET'])
# def dynamic(request):
#     mem = psutil.virtual_memory()
#     available_memory = round(mem.available / (1024**3), 2)
#     used_memory = round(mem.used / (1024**3), 2)
#     free_memory = round(mem.free / (1024**3), 2)
#     memory_percent = mem.percent
#     # 獲取 CPU 使用率
#     cpu_usage_pre_percent = psutil.cpu_percent(interval=0.3, percpu=True)
#     total = 0
#     for usage in cpu_usage_pre_percent:
#         total += usage
#     cpu_usage_percent = total/len(cpu_usage_pre_percent)

#     data = {
#         'available_memory': available_memory,
#         'used_memory': used_memory,
#         'free_memory': free_memory,
#         'memory_percent': memory_percent,
#         'cpu_usage_pre_percent': cpu_usage_pre_percent,
#         "cpu_usage_percent": cpu_usage_percent
#     }

#     return Response(data)


# @api_view(['GET'])
# def mp3_count(request):
#     mp3_count = 0

#     # 使用os.walk遍歷資料夾中的檔案和子目錄
#     for root, dirs, files in os.walk(settings.FORDERED_PATH):
#         for file in files:

#             # 檢查檔案是否是以.mp3為副檔名
#             if file.lower().endswith(".mp3"):
#                 mp3_count += 1

#     return Response({'count': mp3_count, 'size': get_file_size()})


# def get_file_size():
#     total_size = 0

#     # 使用 os.walk 遍歷資料夾中的檔案和子目錄
#     for root, dirs, files in os.walk(settings.FORDERED_PATH):
#         for file in files:
#             file_path = os.path.join(root, file)
#             total_size += os.path.getsize(file_path)

#     # 將整體大小轉換為人類可讀的格式 (MB)
#     total_size_mb = total_size / (1024 * 1024*1024)

#     # 回傳整體數量和大小
#     return total_size_mb


# @api_view(['GET'])
# def get_network_usage(request):
#     # 初始化網路用量的計數器
#     prev_net_io_counters = psutil.net_io_counters()

#     while True:
#         # 暫停 1 秒
#         time.sleep(1)

#         # 獲取當前的網路用量
#         current_net_io_counters = psutil.net_io_counters()
#         bytes_sent_per_sec = (current_net_io_counters.bytes_sent -
#                               prev_net_io_counters.bytes_sent) / (1024 * 1024)
#         bytes_recv_per_sec = (current_net_io_counters.bytes_recv -
#                               prev_net_io_counters.bytes_recv) / (1024 * 1024)

#         # 將網路用量轉換為 MB 並取小數點後兩位
#         bytes_sent_per_sec_mb = round(bytes_sent_per_sec, 2)
#         bytes_recv_per_sec_mb = round(bytes_recv_per_sec, 2)

#         # 更新計數器
#         prev_net_io_counters = current_net_io_counters

#         # 構建回傳的資料字典
#         response_data = {
#             'bytes_sent_per_sec_mb': bytes_sent_per_sec_mb,
#             'bytes_recv_per_sec_mb': bytes_recv_per_sec_mb,
#         }

#         # 返回回傳的資料
#         return Response(response_data)


# class AdminIView(APIView):
#     def get(self, request,):
#         try:
#             count = AdminCount.objects.using("user").all().first()
#             serializer = AdminSerializer(count)
#             return Response(serializer.data)
#         except AdminCount.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request):
#         # Delete all data in AdminCount
#         AdminCount.objects.using("user").all().delete()

#         # get data
#         artist_count = Artist.objects.using("music").all().count()
#         song_count = Song.objects.using("music").all().count()
#         user_count = Profile.objects.using("user").all().count()
#         style_count = StyleTitle.objects.using("music").all().count()
#         dow_count = DowARtist.objects.using("music").all().count()

#         # Create
#         AdminCount.objects.using("user").create(
#             artist=artist_count, song=song_count, style=style_count, dow=dow_count, user=user_count)

#         return Response({"success": True}, status=status.HTTP_200_OK)
