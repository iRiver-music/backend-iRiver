from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from .models import Profile, Setting, EQ, Playlist, ListeningHistory

# 異步版本

from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async


def login(request):
    return True


@api_view(["GET"])
def listeningHistory(request, music_ID):
    try:
        listening_record = ListeningHistory.objects.using(
            "user").get(music_ID=music_ID)
    except ListeningHistory.DoesNotExist:
        return Response({"message": "找不到指定的聽歌紀錄"}, status=404)

    # 將找到的聽歌紀錄的 count 屬性加一
    listening_record.count += 1
    listening_record.save(using="user")

    return Response({"message": "聽歌紀錄的 count 屬性已經加一"}, status=200)
