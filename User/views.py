from django.conf import settings
from django.http import JsonResponse, FileResponse
import os
import random
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.db import connections

from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.Authentication.authentication import FirebaseAuthentication


# models
from Music.models import Artist, Song
from User.models import EQ, Contract, LastUsersong, ListeningHistory, Playlist, Profile, SearchHistory, Setting
from .serializers import PlaylistSetSerializer, SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer, LastUsersongSerializer
from .function import printcolorhaveline, nowtime, switch_key

# 異步版本
from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view, authentication_classes

# USR RESOURCE


@api_view(["GET"])
# @authentication_classes([FirebaseAuthentication])
def listeningHistory(request, music_ID):
    if not ListeningHistory.objects.filter(music_ID=music_ID).exists():
        listening_record = ListeningHistory.objects.create(music_ID=music_ID)
        return Response({"mes": "ok"}, status=200)
    else:
        listening_record = ListeningHistory.objects.get(music_ID=music_ID)
        listening_record.count += 1
        listening_record.save()
        return Response({"mes": "ok"}, status=200)


@api_view(["GET"])
# @authentication_classes([FirebaseAuthentication])
def searchHistory(request, uid, query):
    SearchHistory.objects.create(uid=uid, query=query)
    return Response({"mes": "ok"}, status=200)


@api_view(["GET"])
# @authentication_classes([FirebaseAuthentication])
def playlistSet(request, uid):
    playlists = Playlist.objects.filter(uid=uid)
    serializer = PlaylistSetSerializer(playlists, many=True)
    return Response(serializer.data)


# contract =================================================================


@api_view(["GET"])
@authentication_classes([FirebaseAuthentication])
def contract(request, uid):
    try:
        if Profile.objects.filter(uid=uid).exists():
            Contract.objects.create(uid=uid)
            return Response({"mes": "ok"}, status=200)
        else:
            return Response({"mes": "uid not exist"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=404)


# last song  =================================================================================================


class LastuserSongAPIView(APIView):
    # authentication_firebase
    def get(slef, request,  uid):
        try:
            obj = LastUsersong.objects.get(uid=uid)
            data = LastUsersongSerializer(obj).data
            return Response(data)

        except Exception as e:
            return Response({"mes": str(e)}, status=404)

    def post(self, request, uid):
        try:
            # delete old
            LastUsersong.objects.delete(uid=uid)

            # create new
            obj = Song.objects.get(music_ID=request.data["music_ID"])
            LastUsersong.objects.create(
                uid=uid, artist=obj.artist, music_ID=request.data["music_ID"])

            return Response({"mes": "ok"})
        except Exception as e:
            return Response({"mes": str(e)}, status=404)


# user img ============================================================


@api_view(['GET'])
def user_playlist_img(request, uid, playlist):
    # 构建用户图片目录路径
    user_img_path = os.path.join(
        settings.BASE_DIR, 'static', 'user', str(uid), f"{playlist}.jpg")

    # 检查用户图片目录是否存在
    if os.path.exists(user_img_path):
        with open(user_img_path, 'rb') as img_file:
            response = FileResponse(img_file)
            return response

    # 如果用户图片目录不存在或没有图片文件，从random目录中随机选择一个.jpg文件并返回该图片
    random_img_dir = os.path.join(
        settings.BASE_DIR, 'static', 'user', 'random')
    random_img_files = [f for f in os.listdir(
        random_img_dir) if f.endswith('.jpg')]

    if random_img_files:
        try:
            selected_random_img = random.choice(random_img_files)
            random_img_path = os.path.join(random_img_dir, selected_random_img)
            with open(random_img_path, 'rb') as img_file:
                response = HttpResponse(content_type='image/jpeg')
                response['Content-Disposition'] = f'attachment; filename="{selected_random_img}"'
                response.write(img_file.read())
                return response
        except Exception as e:
            print(e)

    # 如果连random目录中都没有.jpg文件，返回默认图片或错误信息，根据需要进行修改
    return HttpResponse('No images found.', status=404)

# user music_ID =============================================================


@api_view(['GET'])
def music_ID(request, uid):
    obj = Playlist.objects.filter(
        uid=uid, playlist="fav").values('music_ID', "id").distinct()

    return Response(obj)


@api_view(['GET'])
def creat_test_user(request):
    Profile.objects.create(uid="123")
    EQ.objects.create(uid="123")
    Setting.objects.create(uid="123")

    return Response({"mes": "ok"})
