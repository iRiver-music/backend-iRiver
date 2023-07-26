# import models
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

# self import
from .models import Social,Profile,EQ,Setting,musicList

# program START
test=False # only for testing
url="https://iriver.ddns.net"
localurl="http://127.0.0.1:8000" # only for testing

client_id="1026795084542-4faa7ard63anna4utjtmavuvbe4t4mf4.apps.googleusercontent.com"
client_secret="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"
scope="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
access_type="offline"
include_granted_scopes="true"
response_type="code"

line_client_id="1661190797"
line_client_secret="3fc12add18f596c2597c993f1f858acf"
line_response_type="code"
line_scopes=["profile","openid","email"]

apple_client_id="1661190797"
apple_client_secret="3fc12add18f596c2597c993f1f858acf"
apple_response_type="code"
apple_scopes=["profile","openid","email"]

if test:
    # 測試用環境
    urlgoogle=localurl+"/complete/google/"
    urlline=localurl+"/complete/line/"
    urlapple=localurl+"/complete/apple/"
else:
    # 正式環境
    urlgoogle=url+"/complete/google/"
    urlline=url+"/complete/line/"
    urlapple=url+"/complete/apple/"

# printcolor 函式：在終端機中以不同顏色打印文字
def printcolor(color,text):
    # 根据传入的颜色选择相应的 ANSI 转义码
    if color=="header": # 目前無用
        colorcode="\033[95m"
    elif color=="blue": # 目前無用
        colorcode="\033[94m"
    elif color=="green": # 用於通過 完成 成功 等等
        colorcode="\033[92m"
    elif color=="warning": # 用於用戶驗證失敗 用戶導致的錯誤 等等
        colorcode="\033[93m"
    elif color=="fail": # 用於程式錯誤 重大錯誤 驗證錯誤 等等
        colorcode="\033[91m"
    else:
        printcolor("fail","color error")
        colorcode="\033[95m"
        # raise ValueError("Unsupported color.")

    # 打印带有颜色的文本
    print(str(colorcode)+str(text)+str("\033[0m"))

# printcolorhaveline 函式：在終端機中打印分隔線並打印文字
def printcolorhaveline(color="green",text="",linestyle="-"):
    print(linestyle*30)
    printcolor(color,text)

def nowtime():
    localtime=time.localtime() # 現在時間
    nowtime=time.strftime("%Y-%m-%d %H:%M:%S",localtime) # 轉成date format
    return nowtime

# 登入
def loginsql(request,method,email,password,token=""):
    if method=="google":
        google(request)
    elif method=="line":
        line(request)
    elif method=="apple":
        apple(request)
    elif method=="normal":
        login(request,email,password)
    else:
        printcolorhaveline("fail","loginmethod error")

def google(request):
    googleurl(request)
    googlecallback(request)
    pass

def line(request):
    lineurl(request)
    linecallback(request)
    pass

def apple(request):
    appleurl(request)
    applecallback(request)
    pass

# 登入
def userlogin(request):
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
            printcolorhaveline("green","register success!","-")
            return redirect('/user/data/')  # 重新導向到首頁
        else:
            success=False
            printcolorhaveline("fail","register fail","-")

        return HttpResponse(json.dumps({
            "success": success,
            "data": data
        }))# 要回傳什麼?

# switch_key 函式：根據鍵的格式返回對應的鍵值
def switch_key(tkey):
    if tkey.startswith("#"):
        key=tkey[1:]
    else:
        key=tkey.split("@")[0]
    return key

def getusetemail(accesstoken,channel):
    # 獲取 id_token
    headers={"Authorization": "Bearer "+str(accesstoken)}
    response=requests.post("https://api.line.me/oauth2/v2.1/verify",headers=headers) # 發送 POST 請求，驗證 id_token 並獲取驗證結果
    idtoken=response.json().get("id_token")  # 獲取 id_token
    # 解碼 id_token 並獲取用戶郵件地址
    decodedidtoken=jwt.decode(idtoken.encode("utf-8"),channel,algorithms=["HS256"],options={"verify_signature": False})# 解碼 id_token
    user_email=decodedidtoken.get("email")
    return user_email

def linedata(accesstoken):
    headers={"Authorization": "Bearer "+str(accesstoken)}
    # 發送 GET 請求，獲取 Line 用戶資料
    response=requests.get("https://api.line.me/v2/profile",headers=headers)
    data=response.json()
    return data

def googledata(accesstoken):
    headers={"Authorization": "Bearer "+str(accesstoken)}
    params={"personFields": "photos"}
    # 發送 GET 請求，獲取 Google 用戶資料
    response=requests.get("https://people.googleapis.com/v1/people/me",headers=headers,params=params)
    if response.status_code==200:
        data=response.json()
        return data
    return None

def avatarurl(accesstoken):
    headers={"Authorization": "Bearer "+str(accesstoken)}
    params={"personFields": "photos"}
    # 發送 GET 請求，獲取 Google 用戶資料
    response=requests.get("https://people.googleapis.com/v1/people/me",headers=headers,params=params)
    if response.status_code==200:
        data=response.json()
        photos=data.get("photos",[])
        if photos:
            avatar_url=photos[0].get("url")  # 獲取頭像 URL
            return avatar_url
    return None

def userdata(request):
    if request.method =="POST":
        return HttpResponse(json.dumps({
            "success": True,
            "user_data": request.session["user_data"],
            "user_playlists": request.session["user_playlist"],
        }))
    else:
        return HttpResponse("error")

# save_session 函式：保存用戶會話數據
def save_session(request,name,email,uid,userimageurl):
    request.session["key"]=uid # 保存會話鍵
    request.session["name"]=name # 保存用戶名
    request.session["email"]=email # 保存郵件地址
    request.session["uid"]=uid # 保存用戶 ID
    request.session["user_img_url"]=userimageurl # 保存用戶頭像 URL

    # 創建 SQL 使用者實例
    request.session["user_data"]={"name": name}  # 保存用戶數據
    # 創建 SQL 音樂實例

    # 獲取用戶播放列表
    musicList._meta.db_table=uid
    miuscrow=musicList.objects.using("usermusic").all()

    if miuscrow:
        musicList._meta.db_table=uid
        userplaylistrow=musicList.objects.using("usermusic").values_list('playlist',flat=True).distinct()
    else:
        userplaylistrow=None

    request.session["user_playlist"]=userplaylistrow # 保存用戶播放列表

    # eq
    musicList._meta.db_table=uid
    eqrow=EQ.objects.using("user").filter(UID_EQ=uid).all()
    request.session["user_eq"]=eqrow  # 保存用戶均衡器設置

    # setting
    musicList._meta.db_table=uid
    settingrow=Setting.objects.using("user").filter(UID_SETTING=uid).all()[0]
    setting={
        "UID_SETTING":settingrow[0],
        "LANGUAGE":settingrow[1],
        "SHOW_MODAL":settingrow[2],
        "AUDIO_QUALITY":settingrow[3],
        "AUDIO_AUTO_PLAY":settingrow[4],
        "WIFI_AUTO_DOWNLOAD":settingrow[5],
        "CREATED_AT":settingrow[6].strftime("%Y-%m-%d %H:%M:%S")
    }
    request.session["user_setting"]=setting  # 保存用戶設置

    request.session.save()
    printcolorhaveline("green","save session "+str(request.session["user_data"])+str(request.session["user_playlist"]),"#")
    return JsonResponse({"success": True})

def get_user_session(request):
    uid=request.session["key"]
    if request.method =="POST":
        data=json.loads(request.body)  # 解析 JSON 數據
        get=data.get("get")  # 獲取操作類型

        if get=="user_eq":
            body={"user_eq": request.session["user_eq"]}  # 返回用戶均衡器設置
        elif get=="user_setting":
            body={"user_setting": request.session["user_setting"]}  # 返回用戶設置
        elif get=="user_show_data":
            body={
                "user_data": request.session["user_data"],# 返回用戶數據
                "user_playlists": request.session["user_playlist"],# 返回用戶播放列表
                "user_img": request.session["user_img_url"],# 返回用戶頭像 URL
            }
        elif get=="all":
            body={
                "user_data": request.session["user_data"],# 返回用戶數據
                "user_playlists": request.session["user_playlist"],# 返回用戶播放列表
                "user_img_url": request.session["user_img_url"],# 返回用戶頭像 URL
                "user_eq": request.session["user_eq"],# 返回用戶均衡器設置
                "user_setting": request.session["user_setting"],# 返回用戶設置
            }
        else:
            return HttpResponse("error")

        printcolorhaveline(text=body)
        return HttpResponse(json.dumps({
            "success": True,
            "data": body
        }))
    else:
        return HttpResponse("error")

# userplaylist(未完成)
def get_user_music_list(request):
    uid=request.session["key"]
    playlist="我的最愛"

    data=json.loads(request.body)  # 解析 JSON 數據
    method=data.get("method")  # 獲取操作類型

    if method=="insert": # 插入音樂到播放列表
        music_ID_list=json.dumps([data.get("music_ID")],indent=4)
        music_list=data.get("playlist",playlist)
        printcolorhaveline("green",music_list," ")
        try:
            music_ID_list=json.loads(music_ID_list)
            for music_ID in music_ID_list:
                printcolorhaveline("green","add ",music_ID,"=> ",music_list," ")
                # 查询数据库中是否已存在相同的 music_ID
                musicList._meta.db_table=uid
                row=musicList.objects.using("usermusic").filter(music_ID=music_ID,playlist=music_list).count()
                if row==0: # 不存在则插入新数据
                    musicList._meta.db_table=uid
                    musicList.objects.using("usermusic").create(
                        playlist=music_list,
                        music_ID=music_ID,
                        favorite=False
                    )
                if music_list==playlist: # 如果是我的最愛或在最愛裡面，則將favorite設為true
                    musicList._meta.db_table=uid
                    musicList.objects.using("usermusic").filter(music_ID=music_ID).update(favorite=True)
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="get": # 獲取播放列表中的音樂
        musicList._meta.db_table=uid
        row=musicList.objects.using("usermusic").filter(playlist=music_list).order_by('-created_at').values_list('music_ID',flat=True)
        return JsonResponse(list(row),safe=False)
    elif method=="delete": # 從播放列表中刪除音樂
        try:
            music_ID_list=json.dumps([data.get("music_ID")],indent=4)
            music_list=data.get("playlist",playlist)
            music_ID_list=json.loads(music_ID_list) # 解析list
            # 删除每个id
            for music_ID in music_ID_list:
                musicList._meta.db_table=uid
                musicList.objects.using("usermusic").filter(playlist=music_list,music_ID=music_ID).delete()
                # 如果是我的最愛，則將favorite設為false
                if music_list==1:
                    musicList._meta.db_table=uid
                    musicList.objects.using("usermusic").filter(music_ID=music_ID).update(favorite=False)
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="delete_playlist": # 刪除播放列表
        try:
            playlist=data.get("playlist",playlist)
            musicList._meta.db_table=uid
            musicList.objects.using("usermusic").filter(playlist=playlist).delete()
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="create_playlist": # 創建播放列表
        playlist=data.get("playlist",playlist)
        try:
            musicList._meta.db_table=uid
            musicList.objects.using("usermusic").create(
                playlist=playlist,
                music_ID="",
                favorite="",
            ).save()
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success": success}),safe=False)
    elif method=="get_playlist": # 獲取所有播放列表
        musicList._meta.db_table=uid
        countrow=musicList.objects.using("usermusic").count()
        musicList._meta.db_table=uid
        row=musicList.objects.using("usermusic").exclude(playlist='我的最愛').values_list('playlist',flat=True).distinct().all()
        if row:
            check=row
        else:
            check=None
        return JsonResponse(json.dumps({"success": True,"playlists": check}),safe=False)
    else:
        return JsonResponse({"success": False})


# 註冊(已完成)
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
            printcolorhaveline("green","register success!","-")
        else:
            success=False
            body=""
            printcolorhaveline("fail","register fail(register duplicate)","-")

        return HttpResponse(json.dumps({
            "success": success,
            "data": body
        }))# 要回傳什麼?

# 登出(已完成)
def logout(request,uid):
    # logout(request)
    request.session['isLogin']=False
    request.session.save()
    printcolorhaveline("green",str(uid)+" 登出成功"," ")
    return redirect('/user/login')

# base 函式：處理用戶登入的基本操作
def base(userid,email,name,userimageurl,request):
    row=Social.objects.using("user").filter(email=email).all()

    if len(row)>0:
        uid=row[0].uid
    else: # 無帳號
        printcolorhaveline("green","create user","-")
        uid=uuid.uuid4()
        uid_str=str(uid).replace("-","")
        short_uid="a"+uid_str[:12]
        uid=short_uid
        # 創建帳號所需資料表及欄位
        Social.objects.using("user").create(
            userid=userid,
            email=email,
            uid=uid
        ).save()

        Profile.objects.using("user").create(
            id=uid,
            email=email,
            username=name,
            phone="",
            country="",
            birthday="",
            gender="",
            user_img_url="",
            test=0,
            level=0
        ).save()

        EQ.objects.using("user").create(
            UID_EQ=uid,
            ENGANCE_HIGH=False,
            ENGANCE_MIDDLE=False,
            ENGANCE_LOW=False,
            ENGANCE_HEAVY=False,
            STYLE="null",
            EQ_HIGH=50,
            EQ_MIDDLE=50,
            EQ_LOW=50,
            EQ_HEAVY=50,
            EQ_DISTORTION=0,
            EQ_ZIP=0,
            SPATIAL_AUDIO="null"
        ).save()

        Setting.objects.using("user").create(
            UID_SETTING=uid,
            LANGUAGE="ch",
            SHOW_MODAL="auto",
            AUDIO_QUALITY="auto",
            AUDIO_AUTO_PLAY=1,
            WIFI_AUTO_DOWNLOAD=1,
            CREATED_AT=nowtime()
        ).save()

    save_session(request,name,email,uid,userimageurl)
    printcolorhaveline("green","finish baseing"," ")

def usersavesession(request):
    return save_session(request,request.session["name"],request.session["email"],request.session["key"],request.session["user_img_url"])

def getuserdata(request):
    if request.method == 'POST':
        return HttpResponse(json.dumps({
            "success": True,
            "user_data": request.session['user_data'],
            "user_playlists": request.session['user_playlist'],
        }))
    else:
        return HttpResponse('error')

def checklogin(request):
    if request.session["isLogin"]:
        return JsonResponse({"isLogin": request.session["isLogin"]})
    else:
        return JsonResponse({"isLogin": False})

# google 登入
def googleurl(request):
    state=str(uuid.uuid4()) # 保存 state 至 session 中，以防止 CSRF 攻擊
    # 这一行生成一个随机的UUID作为状态码，并将其转换为字符串。这个状态码用于防止跨站请求伪造(CSRF)攻击，并将其保存在会话(session)中。
    request.session["oauth_state"]=state # 将生成的状态码存储在请求的会话中，以便后续验证请求的合法性。
    url=f"https://accounts.google.com/o/oauth2/v2/auth?scope={scope}&access_type={access_type}&include_granted_scopes={include_granted_scopes}&response_type={response_type}&state={state}&redirect_uri={urlgoogle}&client_id={client_id}" # 生成 Google 登入連結
    return HttpResponseRedirect(url)

def googlecallback(request):
    success=False
    code=request.GET.get("code")
    state=request.GET.get("state")
    if code and state==request.session.get("oauth_state"): # 检查code和state是否存在，并且state的值与之前保存在会话中的oauth_state相匹配。
        url="https://oauth2.googleapis.com/token"
        params={
            "code": code,# 授权码
            "client_id": client_id,# 客户端ID
            "client_secret": client_secret,# 客户端密钥
            "redirect_uri": urlgoogle,# 回调URL
            "grant_type": "authorization_code" # 授权类型
        }
        # 向 Google API 發送 POST 請求，獲取存取令牌
        response=requests.post(url,data=params) # 设置向Google API发送POST请求的URL和参数
        token_data=response.json()

        id_token=token_data.get("id_token",None) # 从响应的JSON数据中提取出ID令牌
        access_token=token_data.get("access_token",None) # 访问令牌

        url="https://oauth2.googleapis.com/tokeninfo"
        data={ "id_token": id_token }

        response=requests.get(url,params=data) # 向 Google API 發送 GET 請求，獲取使用者資料
        data=response.json()
        email=data["email"]
        picture=data["picture"]
        userid=data["sub"]
        name=data["name"]
        # 使用requests.get方法向Google API发送GET请求，获取用户的详细信息。然后从响应的JSON数据中提取出用户的电子邮件(email)、头像(picture)、用户ID(sub)和姓名(name)。

        base(userid,email,name,picture,request) # 調用 base 函式進行處理 将获取到的用户信息传递给它进行处理。
        success=True
    else:
        printcolor("warning","google驗證失敗")
    request.session["isLogin"]=success # 将isLogin标志保存到会话中，以便在其他地方可以使用。
    if success:
        printcolorhaveline("green","google登入成功")
        return redirect("/music/discover/") # 重定向到"/music/discover/"页面
    else:
        printcolorhaveline("warning","google登入失敗")
        return redirect("/user/login/") # 重定向到"/user/login/"页面。

# line 登入
def lineurl(request):
    state=str(uuid.uuid4())
    # 保存 state 至 session 中，以防止 CSRF 攻擊
    request.session["oauth_state"]=state
    # 生成 Line 登入連結
    encoded_scopes=urllib.parse.quote(" ".join(line_scopes))
    url=f"https://access.line.me/oauth2/v2.1/authorize?response_type={line_response_type}&client_id={line_client_id}&redirect_uri={urlline}&state={state}&scope={encoded_scopes}"
    return HttpResponseRedirect(url)

def linecallback(request):
    success=False
    code=request.GET.get("code")
    state=request.GET.get("state")
    if code and state==request.session.get("oauth_state"):
        url="https://api.line.me/oauth2/v2.1/token"
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": urlline,
            "client_id": line_client_id,
            "client_secret": line_client_secret,
        }
        # 向 Line API 發送 POST 請求，獲取存取令牌
        response=requests.post(url,data)
        token_data=response.json()
        id_token=token_data.get("id_token",None)
        access_token=token_data.get("access_token",None)

        url="https://api.line.me/oauth2/v2.1/verify"
        data={
            "id_token": id_token,
            "client_id": line_client_id,
        }
        # 向 Line API 發送 POST 請求，獲取用戶資料
        response=requests.post(url,data=data)
        data=response.json()
        email=data["email"]
        picture=data["picture"]
        userid=data["sub"]
        name=data["name"]

        # 調用 base 函式進行處理
        base(userid,email,name,picture,request)
        success= True
    else:
        print("驗證失敗")

    request.session["isLogin"]=success
    if success:
        printcolorhaveline(text="登入成功")
        return redirect("/music/discover/")
    else:
        printcolorhaveline(text="登入失敗")
        return redirect("/user/login/")

def appleurl(request):
    pass

def applecallback(request):
    pass

# 個人資料
def profileget(request,uid):
    if request.method=="GET":
        # 查詢用戶
        body=json.loads(request.body)
        uid=request.session["key"]
        row=Profile.objects.using("user").filter(id=uid).all()
        data=""
        if row:
            row=row[0]
            data={
                "id": row[0],
                "email": row[1],
                "username": row[2],
                "phone": row[3],
                "country": row[4],
                "birthday": row[5],
                "gender": row[6],
                "user_img_url": row[7],
                "test": row[8],
                "level": row[9],
            }
            printcolorhaveline("green",data,"-")
        else:
            data=None
        return render(request,"edit_profile.html",{"form": data})
    else:
        printcolorhaveline("fail","method error","-")

def profilepost(request):
    if request.method=="PUT":
        # data
        id=request.session["key"]
        data=request.body.decode('utf-8')
        data_dict=json.loads(data)
        value=data_dict.get('value')
        newvalue=data_dict.get('newValue')
        # 根據 id 找到對應的記錄
        query=Profile.objects.using("user").get(id=id)
        setattr(query,value,newvalue) # 更新記錄的各個欄位
        query.save()
        printcolorhaveline("green","成功修改 "+str(id)+" 的資料","-")
        return redirect("/user/profile/")
    else:
        printcolorhaveline("fail","method error","-")

def user_setting(request):
    if request.method=="PUT":
        uid=request.session["key"]
        data=request.body.decode('utf-8')
        # 是這樣拿值嗎?
        data_dict=json.loads(data)
        value=data_dict.get('value')
        newvalue=data_dict.get('newValue')
        print(value,newvalue)
        # query=""
        query=Setting.objects.using("user").get(UID_SETTING=uid)
        setattr(query,value,newvalue)
        query.save()
        # body=json.loads(request.body)
    #     method=body.get("method")
    #     kwargs=body.get("kwargs")
    #     row=False
    #     if method=="insert":
    #         query=EQ.objects.using("user").get_or_create(
    #             UID_SETTING=uid,
    #             defaults={
    #                 'LANGUAGE': "ch",
    #                 'SHOW_MODAL': "auto",
    #                 'AUDIO_QUALITY': "auto",
    #                 'AUDIO_AUTO_PLAY': 1,
    #                 'WIFI_AUTO_DOWNLOAD': 1,
    #                 'CREATED_AT': nowtime()
    #             }
    #         )
    #         row=query
    #     elif method=="update":
    #         column=kwargs["column"]
    #         newvalue=kwargs["new_value"]
    #         printcolorhaveline("green",kwargs,"-")

    #         query=Setting.objects.using("user").get(UID_SETTING=uid)
    #         setattr(query,column,newvalue)
    #         query.save()
    #         row=query
    #     elif method=="select":
    #         row=Setting.objects.using("user").filter(UID_EQ=uid).all()
    #     else:
    #         printcolorhaveline("fail",f"the method {method} is not supported","-")
        row=query
        return JsonResponse({"data": row })
    else:
        return JsonResponse({"success": False})

def user_eq(request):
    if request.method=="PUT":
        uid=request.session["key"]
        data=request.body.decode('utf-8')
        data_dict=json.loads(data)
        # 是這樣拿值嗎?
        value=data_dict.get('value')
        newvalue=data_dict.get('newValue')
        # column=kwargs["column"]
        # newvalue=kwargs["new_value"]
        # printcolorhaveline("green",kwargs,"-")
        query=EQ.objects.using("user").get(UID_EQ=uid)
        # 更新記錄的各個欄位
        setattr(query,value,newvalue)
        query.save()
        row=query
        # body=json.loads(request.body)
        # kwargs=body.get("kwargs")
        # method=body.get("method")
        # printcolorhaveline("green",kwargs)
        # row=False
        # if method=="insert":
        #     query=EQ.objects.using("user").get_or_create(
        #         UID_EQ=kwargs["UID_EQ"],
        #         defaults={
        #             'ENGANCE_HIGH': kwargs["ENGANCE_HIGH"],
        #             'ENGANCE_MIDDLE': kwargs["ENGANCE_MIDDLE"],
        #             'ENGANCE_LOW': kwargs["ENGANCE_LOW"],
        #             'ENGANCE_HEAVY': kwargs["ENGANCE_HEAVY"],
        #             'STYLE': kwargs["STYLE"],
        #             'EQ_HIGH': kwargs["EQ_HIGH"],
        #             'EQ_MIDDLE': kwargs["EQ_MIDDLE"],
        #             'EQ_LOW': kwargs["EQ_LOW"],
        #             'EQ_HEAVY': kwargs["EQ_HEAVY"],
        #             'EQ_DISTORTION': kwargs["EQ_DISTORTION"],
        #             'EQ_ZIP': kwargs["EQ_ZIP"],
        #             'SPATIAL_AUDIO': kwargs["SPATIAL_AUDIO"],
        #         }
        #     )
        #     row=query
        # elif method=="update":
        #     column=kwargs["column"]
        #     newvalue=kwargs["new_value"]
        #     printcolorhaveline("green",kwargs,"-")
        #     query=EQ.objects.using("user").get(UID_EQ=kwargs["UID_EQ"])
        #     # 更新記錄的各個欄位
        #     setattr(query,column,newvalue)
        #     query.save()
        #     row=query
        # elif method=="select":
        #     row=EQ.objects.using("user").filter(UID_EQ=kwargs["UID_EQ"]).all()
        # else:
        #     printcolorhaveline("fail",f"the method {method} is not supported","-")

        return JsonResponse({"data": row })
    else:
        return JsonResponse({"success":False})

def my_playlist():
    row=""
    return JsonResponse({"success":False,"data": row })

# 註記
# 如果有任何錯誤直接跟我說即可