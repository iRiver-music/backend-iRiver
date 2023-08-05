import json
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

from User.models import Setting,EQ,Profile
from User.serializers import SettingSerializer,ProfileSerializer,EQSerializer


class UserLoginAPIView(APIView):
    # 一般登入
    def post(self,request):
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
                login(request,user)
            else:
                function.printcolorhaveline("fail","register fail","-")
                # return Response({"message": "login fail"},status=status.HTTP_200_OK)
            return Response({"message": "login successfully"},status=status.HTTP_200_OK)

    # 第三方登入
    def google(self,request):
        pass

    def line(self,request):
        pass

    def apple(self,request):
        pass