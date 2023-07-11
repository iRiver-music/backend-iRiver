# import
import django
from django.shortcuts import render

# self import
import sql

# program START

# google 登入
def googleurl(request):
    pass

def googlecallback(request):
    pass

# line 登入
def lineurl(request):
    pass

def linecallback(request):
    pass

# 登入
def signup(request):
    if request.method=="POST":
        return ;
    else:
        return "[ERROR]method error"

# 登出
def logout(request):
    if request.method=="GET":
        return ;
    else:
        return "[ERROR]method error"

# 註冊
def signup(request):
    if request.method=="GET":
        return ;
    else:
        return "[ERROR]method error"

# 個人資料
def setting():
    pass