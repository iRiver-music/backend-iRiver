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

from User.Authentication.authentication import FirebaseAuthentication

from .serializers import PlaylistSetSerializer, SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from .models import Profile, Setting, EQ, Playlist, ListeningHistory, Social, Contract, SearchHistory
from .function import printcolorhaveline, nowtime, switch_key

# 異步版本
from drfa.decorators import api_view, APIView
from asgiref.sync import sync_to_async
from rest_framework.decorators import api_view, authentication_classes


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
# @authentication_classes([FirebaseAuthentication])
def contract(request, uid):
    try:
        if Profile.objects.filter(uid=uid).exists():
            Contract.objects.create(uid=uid)
            return Response({"mes": "ok"}, status=200)
        else:
            return Response({"mes": "uid not exist"}, status=404)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=404)


@api_view(['GET'])
def creat_test_user(request):
    Profile.objects.create(uid="123")
    EQ.objects.create(uid="123")
    Setting.objects.create(uid="123")

    return Response({"mes": "ok"})
