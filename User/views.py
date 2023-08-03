import json
import time
import difflib
import jwt
import requests
import uuid
import urllib.parse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from httplib2 import Authentication
from django.contrib.auth import authenticate,login,logout
from django.db import connections

from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SettingSerializer,ProfileSerializer,EQSerializer,PlaylistSerializer
from .models import Profile,Setting,EQ,Playlist,ListeningHistory,Social
import function

# 異步版本
from drfa.decorators import api_view,APIView
from asgiref.sync import sync_to_async

# 登入(未測試)
def login(request):
    if request.method=="POST": # (CSRF cookie not set.)
        data=json.loads(request.body)
        """
        假定json格式為
        {
            "username": str,
            "password": str
        }
        """
        user=authenticate(username=data["username"],password=data["password"])
        if user!=None:
            success=True
            login(request,user)
            function.printcolorhaveline("green","register success!","-")
            return redirect('/user/data/')  # 重新導向到首頁
        else:
            success=False
            function.printcolorhaveline("fail","register fail","-")

        return HttpResponse(json.dumps({
            "success": success,
            "data": data
        }))# 要回傳什麼?

# 註冊(未測試)
def register(request):
    if request.method=="GET":
        print(request.body)
        data=json.loads(request.body)
        print(data)
        row=User.objects.using("djangouserlocal").filter(username=data["username"]).all()
        success=True
        body=""
        if len(row)==0:
            """
            假定json格式為
            {
                "username": str,
                "email": str,
                "password": str
            }
            """
            user=User.objects.using("djangouserlocal").create(
                is_speruser=0,
                username=data["username"],
                first_name="",
                last_name="",
                email=data["eail"],
                is_staff=0,
                is_active=1,
            )
            user.set_password(data["password"])
            user.save()
            success=True
            body=data
            function.printcolorhaveline("green","register success!","-")
        else:
            success=False
            body=""
            function.printcolorhaveline("fail","register fail(register duplicate)","-")

        return HttpResponse(json.dumps({
            "success": success,
            "data": body
        }))# 要回傳什麼?

# 登出(未測試)
def logout(request,uid):
    request.session['isLogin']=False
    request.session.save()
    function.printcolorhaveline("green",str(uid)+" 登出成功"," ")
    return redirect('/user/login')

# 刪除帳號(未測試)
def delaccount(request,uid):
    Profile.objects.using("user").filter(id=uid).delete()
    Setting.objects.using("user").filter(id=uid).delete()
    EQ.objects.using("user").filter(id=uid).delete()
    Social.objects.using("user").filter(uid=uid).delete()
    request.session['isLogin']=False
    request.session.save()
    function.printcolorhaveline("green",str(uid)+"刪除成功"," ")
    return redirect('/user/login')

@api_view(["GET"])
def listeningHistory(request,music_ID):
    try:
        listening_record=ListeningHistory.objects.get(music_ID=music_ID)
    except ListeningHistory.DoesNotExist:
        return Response({"message": "找不到指定的聽歌紀錄"},status=404)

    # 將找到的聽歌紀錄的 count 屬性加一
    listening_record.count+=1
    listening_record.save()

    return Response({"message": "聽歌紀錄的 count 屬性已經加一"},status=200)
