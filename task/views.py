import base64
from django.shortcuts import render
# 異步版本
from drfa.decorators import api_view, APIView
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Music.models import Artist, DowARtist, Song
from Music.writeJson import make_json_file
from Task.base.TaseBase import BaseTask
from Task.lib.check.check_song_file import check_song_artist_img_and_dow, check_song_file_action
from Task.lib.check.check_task_log_action import check_log_action, check_task_log_action
from Task.lib.mail.send_mail_task import send_mail_action
from Task.lib.style.check import check_style_song
from Task.lib.style.push_style import clean_style, push_style
from Task.lib.style.style import get_style
from Task.lib.update.update_song import update_song_action
from rest_framework.response import Response

# django
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from Task.models import Library, TaskLog

# 自制
from User.Authentication.authentication import HasLevelFivePermission, HasLevelThreePermission
from User.models import Profile
from lib.Email.send import send_style_mail
from django.conf import settings
# job
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler

# base task
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


# initialize =================================================
@api_view(['GET'])
def initialize(request):
    """
    初始化 
    """

    port = 5000
    file_port = 5002
    proj = "iriver"
    file_proj = "couldBox"

    lib_list = [
        {
            "port": port,
            "url": "/task/update_style",
            "proj": proj,
            "desc": "Update the latest song content.  (a mounth)"
        },
        {
            "port": port,
            "url": "/task/update_song",
            "proj": proj,
            "desc": "Check if there are any new songs added to download.   (a week)"
        },
        {
            "port": port,
            "url": "/task/check_style_task",
            "proj": proj,
            "desc": "Check if all the songs in the style table are there, if not, join the download. (a week)"
        },
        {
            "port": port,
            "url": "/task/check_log",
            "proj": proj,
            "desc": "Check all logs and quantities. (a week)"
        },
        {
            "port": port,
            "url": "/task/update_qurey",
            "proj": proj,
            "desc": "update all query json files.  (daily)"
        },

        # file server

        {
            "port": file_port,
            "url": "/task/check_song",
            "proj": file_proj,
            "desc": "Check if all songs and covers are there  (a week)"
        },
        {
            "port": file_port,
            "url": "/task/dow_fail_artist",
            "proj": file_proj,
            "desc": "Dow all fail dow artists.  (a week)"
        },
    ]

    for lib in lib_list:
        Library.objects.create(**lib)

    return Response({"mes": "ok"})

# update =================================================================


@api_view(['POST'])
def update_style(request):
    """
    更新歌曲 
    下載style 
    """
    class update_style_task(BaseTask):
        def __init__(self, task_name,  **opcode_mes):
            super().__init__(task_name, **opcode_mes)

        def run_task(self):
            clean_style()

            get_style()

            push_style()

            check_style_song(request=request)

            send_style_mail()

            super().run_task()

    task = update_style_task(task_name="update_style_task", **request.data)
    task.run()

    return Response({"mes": task.respjson})


@api_view(['POST'])
def update_song(request):
    class update_song_task(BaseTask):
        def __init__(self, task_name,  **opcode_mes):
            super().__init__(task_name, **opcode_mes)

        def run_task(self):
            update_song_task(max_workers=10)

            super().run_task()

    task = update_song_task(task_name="update_song_task", **request.data)
    task.run()

    return Response({"mes": task.respjson})


# # check =================================================================


# @api_view(['POST'])
# def check_style(request):
#     class check_style_task(BaseTask):
#         def __init__(self, task_name,  **opcode_mes):
#             super().__init__(task_name, **opcode_mes)

#         def run_task(self):
#             check_style_song(request=request)

#             super().run_task()

#     task = check_style_task(task_name="check_style_task", **request.data)
#     task.run()

#     return Response({"mes": task.respjson})

# # check DNS

# @api_view(['POST'])
# def check_DNS(request):
#     """
#     更新json檔案
#     """

#     class check_DNS_task(BaseTask):
#         def __init__(self, task_name,  **opcode_mes):
#             super().__init__(task_name, **opcode_mes)

#         def run_task(self):
#             # check_DNS_task_action()

#             super().run_task()

#     task = check_DNS_task(task_name="check_DNS_task", **request.data)
#     task.run()

#     return Response({"mes": task.respjson})


# cheack log =================================================================


@api_view(['POST'])
def check_log(request):
    """
    確認所有log 都範圍內
    """
    class check_log_task(BaseTask):
        def __init__(self, task_name,  **opcode_mes):
            super().__init__(task_name, **opcode_mes)

        def run_task(self):
            check_log_action(check_task_log_reglur_day=90,
                             check_track_log_reglur_years=3)

            super().run_task()

    task = check_log_task(task_name="check_log_task", **request.data)
    task.run()

    return Response({"mes": task.respjson})


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasLevelFivePermission])
def update_qurey(request):
    """
    更新json檔案
    """

    class QueryTask(BaseTask):
        def __init__(self, task_name,  **opcode_mes):
            super().__init__(task_name, **opcode_mes)

        def run_task(self):
            make_json_file(request=request)

            super().run_task()

    task = QueryTask(task_name="QueryTask", **request.data)
    task.run()

    return Response({"mes": task.respjson})

# email =================================================================


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasLevelFivePermission])
def sned_mail(request):
    """
    更新json檔案
    """

    class sned_mail_task(BaseTask):
        def __init__(self, task_name,  **opcode_mes):
            super().__init__(task_name, **opcode_mes)

        def run_task(self):
            send_mail_action()

            super().run_task()

    task = sned_mail_task(task_name="sned_mail_task", **request.data)
    task.run()

    return Response({"mes": task.respjson})
# log =================================================================


@api_view(["GET"])
# @permission_classes([IsAuthenticated, HasLevelThreePermission])
def get_task_log(request):
    try:
        log = TaskLog.objects.all().values().order_by("-created_at")

        return JsonResponse({"data": list(log)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["DELETE"])
# @permission_classes([IsAuthenticated, HasLevelThreePermission])
def del_task_log(requset):
    pass


# test = =====================================================================


@api_view(['GET'])
def test(request):
    ok = send_style_mail(who="賴泓瑋", email="lai09150915@gmail.com")
    return Response({"date": 123})


# library =====================================================================


class LibraryView(APIView):
    # @permission_classes([IsAuthenticated, HasLevelThreePermission])
    def get(self, request):
        lib = Library.objects.all().values()

        return Response(lib)

    # @permission_classes([IsAuthenticated, HasLevelThreePermission])
    def post(self, request):
        try:
            print(request.data)
            level_obj = Library.objects.create(**request.data)

            return JsonResponse({'mes': 'Level registered successfully', 'url': level_obj.url}, status=200)

        except Exception as e:
            return JsonResponse({'mes': "An error occurred while registering the lib {}".format(e)}, status=404)

    # @permission_classes([IsAuthenticated, HasLevelFivePermission])
    def delete(self, request):
        try:
            data = request.GET.dict()
            obj = Library.objects.get(id=data["id"]).delete()
            TaskLog.objects.create(
                username=data["username"], opcode=200, source="admin", desc="Deleted {}".format(obj.url))

            return JsonResponse({'mes': 'Library deleted successfully'}, status=200)
        except Library.DoesNotExist:
            return JsonResponse({'mes': "Library not found"}, status=404)
        except Exception as e:
            return JsonResponse({'mes': str(e)}, status=404)

    def put(self, request):
        pass


@api_view(["DELETE"])
def stop_all_tasks(request):
    scheduler.remove_all_jobs()
    # Library.objects.all().delete()
    return Response({"status": "success"})


# job =================================================================
register_events(scheduler)
scheduler.start()
