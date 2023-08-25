from django.shortcuts import render
# 異步版本
from drfa.decorators import api_view, APIView
from h11 import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from Music.models import Artist, Song
from Music.music_db.writeJson import make_json_file
import User

# django
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# 自制
from User.Authentication.authentication import HasLevelFivePermission


# base task
import base.TaskBase as TaskBase
# =================================================================


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasLevelFivePermission])
def update_qurey(request):
    """
    更新json檔案
    """

    class QueryTask(TaskBase):
        def __init__(self, **opcode_mes):
            super().__init__(**opcode_mes)

        def run_task(self):
            make_json_file(request=request)
            self.respjson = {"mes": "QueryTask executed successfully"}

    queryTask = QueryTask(**request.data)
    queryTask.run_task()

    return Response({"mes": queryTask.respjson})


@api_view(['POST'])
@permission_classes([IsAuthenticated, HasLevelFivePermission])
def update_discover_title(request, title):
    """
    更新discover 專輯 必續自選
    """
    pass


# for admin data

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasLevelFivePermission])
def info(request):
    try:
        song_c = Song.objects.all().count()
        artist_c = Artist.objects.all().count()
        user_c = User.objects.all().count()

        return JsonResponse({"song_c": song_c, "artist_c": artist_c, "user_c": user_c})
    except Exception as e:
        return Response({"mes": str(e)}, status=404)
