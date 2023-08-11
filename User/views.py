import json
import time
import difflib
import jwt
import requests
import uuid
import urllib.parse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from httplib2 import Authentication
from django.contrib.auth import authenticate, login, logout
from django.db import connections

from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from .models import Profile, Setting, EQ, Playlist, ListeningHistory, Social
from .function import printcolorhaveline, nowtime, switch_key

# 異步版本
from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async

@api_view(["GET"])
def listeningHistory(request, music_ID):
    try:
        listening_record = ListeningHistory.objects.get(music_ID=music_ID)
    except ListeningHistory.DoesNotExist:
        return Response({"message": "找不到指定的聽歌紀錄"}, status=404)

    # 將找到的聽歌紀錄的 count 屬性加一
    listening_record.count += 1
    listening_record.save()

    return Response({"message": "聽歌紀錄的 count 屬性已經加一"}, status=200)


@api_view(["GET"])
def valid_invitation_code(request, invitation_code):
    if Profile.objects.filter(invitation_code=invitation_code).exists():
        return Response({"message": "check"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"message": "empty"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def contract(request,uid):
    pass
    # try:
    #     contract = request.data["contract"]
    #     if Profile.objects.filter(contract=contract).exists():
    #         return Response({"message": "check"}, status=status.HTTP_202_ACCEPTED)
    #     else:
    #         return Response({"message": "uid not exist"}, status=status.HTTP_404_NOT_FOUND)
    # except:
    #     return Response({"message": "uid not exist"}, status=status.HTTP_404_NOT_FOUND)