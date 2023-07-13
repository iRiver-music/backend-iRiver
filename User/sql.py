# import
import json
import difflib
import jwt
import requests
import uuid
import urllib.parse
import pymysql
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# self import
# none

# program START

# sql 串接
dbuser=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="django_user",charset="utf8") # user 的 db
dbmusic=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="music_db",charset="utf8") # muisc 的 db
dbconfiguser=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="iRiver_user_data",charset="utf8")
dbconfigusermusiclist=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="iRiver_user_music_list",charset="utf8")

# query 的簡化 function
def query(db,query,data=()):
    try:
        row=db.cursor() # 操作游標
        row.execute(query,data) # 匯入data
        db.commit()
        print("success!")
    except Exception as e:
        print("[ERROR]"+str(e))

    row.close()
    db.close()
    return row.fetchall()

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

test=True # only for testing
url="https://iriver.ddns.net"
url="http://127.0.0.1:8000" # only for testing


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

def login():
    pass

# 登出
def logoutsql():
    pass

# 註冊
def signupsql():
    pass

def appleurl(request):
    pass

def applecallback(request):
    pass



###########################################################################












test=True  # 測試模式的標誌，用於根據不同的環境設定相應的參數和配置
formal_url="https://iriver.ddns.net"  # 正式環境的URL
local_url="http://127.0.0.1:8000"  # 本地開發環境的URL
client_id="1026795084542-4faa7ard63anna4utjtmavuvbe4t4mf4.apps.googleusercontent.com"
client_secret="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"
scope="https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
access_type="offline"
include_granted_scopes="true"
response_type="code"
client_id="1661190797"
client_secret="3fc12add18f596c2597c993f1f858acf"
response_type="code"
scopes=["profile","openid","email"]

if test:
    urlgoogle=local_url + "/complete/google/"
    urlline=local_url + "/complete/line/"
else:
    urlgoogle=formal_url + "/complete/google/"
    urlline=formal_url + "/complete/line/"


###########################################################################
# function START

# user/lib::
# switch_key 函式：根據鍵的格式返回對應的鍵值
def switch_key(tkey):
    if tkey.startswith("#"):
        key=tkey[1:]
    else:
        key=tkey.split("@")[0]
    return key

#/data/
# getdata 函式

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

    # 創建用戶音樂列表表格（如果不存在）
    sql=f"""
        CREATE TABLE IF NOT EXISTS uid(
            playlist VARCHAR(255) NOT NULL,
            music_ID VARCHAR(32) NOT NULL,
            favorite BOOLEAN NOT NULL DEFAULT false,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    query(dbconfigusermusiclist,sql)

    # 獲取用戶播放列表
    miuscrow="SELECT*FROM "+uid

    if miuscrow:
        userplaylistrow=query(dbconfigusermusiclist,"SELECT DISTINCT `playlist` FROM "+uid)
    else:
        userplaylistrow=None

    request.session["user_playlist"]=userplaylistrow # 保存用戶播放列表

    # eq
    eqrow=query(dbconfiguser,"SELECT*FROM `user_setting_eq` WHERE `UID_EQ`=%s",(uid))
    request.session["user_eq"]=eqrow  # 保存用戶均衡器設置

    # setting
    settingrow=query(dbconfiguser,"SELECT*FROM `user_setting` WHERE `UID_SETTING`=%s",(uid))[0]
    request.session["user_setting"]=settingrow  # 保存用戶設置

    request.session.save()
    printcolorhaveline("green","save session "+str(request.getsession["user_data"])+str(request.session["user_playlist"]),"#")
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
                "user_data": request.session["user_data"], # 返回用戶數據
                "user_playlists": request.session["user_playlist"], # 返回用戶播放列表
                "user_img": request.session["user_img_url"], # 返回用戶頭像 URL
            }
        elif get=="all":
            body={
                "user_data": request.session["user_data"], # 返回用戶數據
                "user_playlists": request.session["user_playlist"], # 返回用戶播放列表
                "user_img_url": request.session["user_img_url"], # 返回用戶頭像 URL
                "user_eq": request.session["user_eq"], # 返回用戶均衡器設置
                "user_setting": request.session["user_setting"], # 返回用戶設置
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
                # select_sql=(f"SELECT COUNT(*) FROM {uid} ""WHERE music_ID=%s AND playlist=%s")
                row=query(dbconfigusermusiclist,"SELECT COUNT(*) FROM "+str(uid)+" WHERE `music_ID`=%s AND `playlist`=%s",(music_ID,music_list))
                if row[0]==0: # 不存在则插入新数据
                    query(dbconfigusermusiclist,"INSERT INTO "+str(uid)+"(`playlist`,`music_ID`,`favorite`)VALUES(%s,%s,%s)",(music_list,music_ID,False))
                if music_list==playlist: # 如果是我的最愛或在最愛裡面，則將favorite設為true
                    query(dbconfigusermusiclist,"UPDATE "+str(uid)+" SET `favorite`=%s WHERE `music_ID`=%s",(True,music_ID))
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="get": # 獲取播放列表中的音樂
        row=query(dbconfigusermusiclist,"SELECT`music_ID`FROM "+str(uid)+" WHERE `playlist`=%s ORDER BY `created_at` DESC",music_list)
        return JsonResponse(list(row),safe=False)
    elif method=="delete": # 從播放列表中刪除音樂
        try:
            music_ID_list=json.dumps([data.get("music_ID")],indent=4)
            music_list=data.get("playlist",playlist)
            music_ID_list=json.loads(music_ID_list) # 解析list
            # 删除每个id
            for music_ID in music_ID_list:
                query(dbconfigusermusiclist,"DELETE FROM "+str(uid)+" WHERE `playlist`=%s AND `music_ID`=%s",(music_list,music_ID))
                # 如果是我的最愛，則將favorite設為false
                if music_list==1:
                    query(dbconfigusermusiclist,"UPDATE "+str(uid)+" SET `favorite`=%s WHERE `music_ID`=%s",(False,music_ID))
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="delete_playlist": # 刪除播放列表
        try:
            playlist=data.get("playlist",playlist)
            query(dbconfigusermusiclist,"DELETE FROM "+str(uid)+" WHERE `playlist`=%s",(playlist))
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success":success}),safe=False)
    elif method=="create_playlist": # 創建播放列表   ### 還沒做
        playlist=data.get("playlist",playlist)
        try:
            # query(dbconfigusermusiclist,"INSERT INTO"+str(uid)+"()VALUES()",())
            success=True
        except Exception as e:
            printcolorhaveline("fail",e,"-")
            success=False
        return JsonResponse(json.dumps({"success": success}),safe=False)
    elif method=="get_playlist": # 獲取所有播放列表
        countrow=query(dbconfigusermusiclist,"SELECT COUNT(*) FROM "+str(uid))[0]
        if countrow[0]==0:
            check=None

        row=query(dbconfigusermusiclist,"SELECT DISTINCT playlist FROM "+str(uid)+" WHERE playlist != '我的最愛'")

        if row:
            check=row
        else:
            check=None
        return JsonResponse(json.dumps({"success": True,"playlists": check}),safe=False)
    else:
        return JsonResponse({"success": False})


# 註冊
# none

########################################################################


# /login/
# base 函式：處理用戶登入的基本操作
def base(userid,email,name,userimageurl,request):
    userrow=query(dbconfiguser,"SELECT `userid` FROM `user_social` WHERE `userid`=%s",(userid))

    # uid=sql.insert(userid,email)
    emailrow=query(dbconfiguser,"SELECT`uid`FROM `user_social` WHERE `email`=%s",(email))
    useridrow=query(dbconfiguser,"SELECT`userid`FROM `user_social` WHERE `userid`=%s",(userid))
    uid=emailrow[0]
    if uid==None:
        uid=uuid.uuid4()
        uid_str=str(uid).replace("-","")
        short_uid="a" + uid_str[:12]
        uid=short_uid

    if not useridrow[0]:
        query(dbconfiguser,"INSERT INTO `user_social`(`userid`,`email`,`uid`)VALUES(%s,%s,%s)",(userid,email,uid))


    if userrow is None: # 檢查是否有帳號
        query(dbconfiguser,"INSERT INTO `user_profile`(`id`,`email`,`username`,`phone`,`country`,`birthday`,`gender`,`user_img_url`,`test`,`level`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(uid,email,name,"","","","","",0,0))
        # query(dbconfiguser,"UPDATE `user_profile` SET `email`=%s,`username`=%s,`phone`=%s,`country`=%s,`birthday`=%s,`gender`=%s,`user_img_url`=%s,`test`=%s,`level`=%s WHERE `id`=%s",(email,name,"","","","","",0,0,uid)) # 不懂這行在幹嘛?

        query(dbconfigusermusiclist,f"""
            CREATE TABLE IF NOT EXISTS {uid}(
                `id` VARCHAR(36) NOT NULL PRIMARY KEY,
                music_ID VARCHAR(32) NOT NULL,
                playlist VARCHAR(255) NOT NULL,
                favorite BOOLEAN NOT NULL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """) # 創建用戶音樂列表表格(如果不存在) ir->user_music_list-///

        # 註冊用戶均衡器
        # sqleq(config=dbconfiguser).register(UID_EQ=uid)

        # 註冊用戶設置
        # sqlusersetting(config=dbconfiguser).register(UID_SETTING=uid)

    # 保存用戶會話數據
    save_session(request,name,email,uid,userimageurl)

    printcolorhaveline("green","finish baseing"," ")
########################################################################

class sqlclass:
    def __init__(self,config):
        self.config=config
        self.table_name=None
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_table(self,tablename):
        printcolorhaveline("green","create class table"+str(tablename),"-")

    def commit(self,method: str,**kwargs):
        if method=="insert":
            self.insert(**kwargs)
        elif method=="update":
            self.updata(**kwargs)
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self,sql: str,values):
        print(values)
        self.show(sql=sql,kwargs=values)
        return self.execute(sql=sql,values=values)

    def update(self,sql: str,values):
        self.show(sql=sql,kwargs=values)
        return self.execute(sql=sql,values=values)

    def select(self,sql: str,values):
        self.show(sql=sql,kwargs=values)
        return self.execute(sql=sql,values=values)

    def execute(self,sql,values,isALL=False):
        self.cursor.execute(sql,values)
        self.db.commit()
        res=self.cursor.fetchall() if isALL else self.cursor.fetchone()
        print("------------------------------")
        print(f"sql {sql} results is {res}")

        if res!=None:
            return res
        else:
            return None

    def show(self,sql,kwargs):
        print("------------------------------")
        print("the sql is {},the kwargs is{}".format(sql,kwargs))

    def close(self):
        self.db.close()

class sqleq(sqlclass):
    def __init__(self,config):
        super().__init__(config)

        self.table_name="user_setting_eq"

    def commit(self,method: str,**kwargs):
        if method=="insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method=="update":
            kwargs=kwargs.get("kwargs")
            return self.update(**kwargs)
        elif method=="select":
            return self.tuple_to_dict(data_tuple=self.select(**kwargs))
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self,**kwargs):
        sql=sql=f"INSERT IGNORE INTO {self.table_name} (UID_EQ,ENGANCE_HIGH,ENGANCE_MIDDLE,ENGANCE_LOW,ENGANCE_HEAVY,STYLE,EQ_HIGH,EQ_MIDDLE,EQ_LOW,EQ_HEAVY,EQ_DISTORTION,EQ_ZIP,SPATIAL_AUDIO) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        return super().insert(sql=sql,values=self.dict_to_tuple(**kwargs))

    def update(self,**kwargs):
        sql=f"UPDATE {self.table_name} SET {kwargs['column']}=%s WHERE UID_EQ=%s"
        return super().update(sql=sql,values=(kwargs["new_value"],kwargs["UID_EQ"]))

    def select(self,**kwargs):
        sql=f"SELECT * FROM {self.table_name} WHERE UID_EQ=%s"
        return super().select(sql=sql,values=(kwargs["UID_EQ"],))

    def regsiter(self,UID_EQ: str):
        self.insert(UID_EQ=UID_EQ,
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
                    )

    def execute(self,sql,values,isALL=False):
        return super().execute(sql,values,isALL)

    def dict_to_tuple(self,**kwargs):
        return (
            kwargs.get("UID_EQ"),
            kwargs.get("ENGANCE_HIGH"),
            kwargs.get("ENGANCE_MIDDLE"),
            kwargs.get("ENGANCE_LOW"),
            kwargs.get("ENGANCE_HEAVY"),
            kwargs.get("STYLE"),
            kwargs.get("EQ_HIGH"),
            kwargs.get("EQ_MIDDLE"),
            kwargs.get("EQ_LOW"),
            kwargs.get("EQ_HEAVY"),
            kwargs.get("EQ_DISTORTION"),
            kwargs.get("EQ_ZIP"),
            kwargs.get("SPATIAL_AUDIO"),
        )

    def tuple_to_dict(self,data_tuple):
        keys=[
            "UID_EQ",
            "ENGANCE_HIGH",
            "ENGANCE_MIDDLE",
            "ENGANCE_LOW",
            "ENGANCE_HEAVY",
            "STYLE",
            "EQ_HIGH",
            "EQ_MIDDLE",
            "EQ_LOW",
            "EQ_HEAVY",
            "EQ_DISTORTION",
            "EQ_ZIP",
            "SPATIAL_AUDIO"
        ]
        return dict(zip(keys,data_tuple))

class sqlusersetting(sqlclass):
    def __init__(self,config):
        super().__init__(config)
        self.table_name="user_setting"

    def commit(self,method: str,**kwargs):
        if method=="insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method=="update":
            kwargs=kwargs.get("kwargs")
            return self.update(**kwargs)
        elif method=="select":
            return self.tuple_to_dict(data_tuple=self.select(**kwargs))
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self,**kwargs):
        sql=f"INSERT INTO {self.table_name} (UID_SETTING,LANGUAGE,SHOW_MODAL,AUDIO_QUALITY,AUDIO_AUTO_PLAY,WIFI_AUTO_DOWNLOAD) VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE UID_SETTING=UID_SETTING"
        return super().insert(sql=sql,values=self.dict_to_tuple(**1))

    def select(self,**kwargs):
        sql=f"SELECT UID_SETTING,LANGUAGE,SHOW_MODAL,AUDIO_QUALITY,AUDIO_AUTO_PLAY,WIFI_AUTO_DOWNLOAD FROM {self.table_name} WHERE UID_SETTING=%s"
        return super().select(sql=sql,values=(kwargs["UID_SETTING"],))

    def update(self,**kwargs):
        printcolorhaveline(text=kwargs)
        sql=f"UPDATE {self.table_name} SET {kwargs['column']}=%s WHERE UID_SETTING=%s"
        return super().update(sql=sql,values=(kwargs["new_value"],kwargs["UID_SETTING"]))

    def regsiter(self,UID_SETTING: str):
        self.insert(UID_SETTING=UID_SETTING,
                    LANGUAGE="ch",
                    SHOW_MODAL="auto",
                    AUDIO_QUALITY="auto",
                    AUDIO_AUTO_PLAY=True,
                    WIFI_AUTO_DOWNLOAD=True
                    )

    def execute(self,sql,values,isALL=False):
        return super().execute(sql,values,isALL)

    def dict_to_tuple(self,**kwargs):
        return (
            kwargs.get("UID_SETTING"),
            kwargs.get("LANGUAGE"),
            kwargs.get("SHOW_MODAL"),
            kwargs.get("AUDIO_QUALITY"),
            kwargs.get("AUDIO_AUTO_PLAY"),
            kwargs.get("WIFI_AUTO_DOWNLOAD"),
        )

    def tuple_to_dict(self,data_tuple):
        keys=[
            "UID_SETTING",
            "LANGUAGE",
            "SHOW_MODAL",
            "AUDIO_QUALITY",
            "AUDIO_AUTO_PLAY",
            "WIFI_AUTO_DOWNLOAD"
        ]
        return dict(zip(keys,data_tuple))

    def __init__(self,config):
        self.config=config
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_tables(self):
        sql=f"""
            CREATE TABLE IF NOT EXISTS user_profile (
                id VARCHAR(36) NOT NULL PRIMARY KEY,
                email VARCHAR(24) NOT NULL,
                username VARCHAR(24) NOT NULL,
                phone VARCHAR(16) NOT NULL,
                country CHAR(2),
                birthday DATE,
                gender CHAR(1),
                user_img_url VARCHAR(255),
                test TINYINT(2) UNSIGNED DEFAULT 0,
                level TINYINT(2) UNSIGNED DEFAULT 0
            )
        """
        self.cursor.execute(sql)

    def save_user_profile(self,**user_profile):
        print("******************************")
        print(user_profile)
        id=user_profile.get("id")
        email=user_profile.get("email")
        username=user_profile.get("username")
        phone=user_profile.get("phone")
        country=user_profile.get("country")
        birthday=user_profile.get("birthday")
        gender=user_profile.get("gender")
        user_img_url=user_profile.get("user_img_url")
        test=user_profile.get("test",0)
        level=user_profile.get("level",0)
        self.cursor.execute( "INSERT INTO `user_profile` (`id`,`email`,`username`,`phone`,`country`,`birthday`,`gender`,`user_img_url`,`test`,`level`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,email,username,phone,country,birthday,gender,user_img_url,test,level))
        self.cursor.execute("UPDATE user_profile SET email=%s,username=%s,phone=%s,country=%s,bir``thday=%s,gender=%s,user_img_url=%s,test=%s,level=%s WHERE id=%s",(email,username,phone,country,birthday,gender,user_img_url,test,level,id))
        self.db.commit()

    def get_user_data(self,uid):
        self.cursor.execute("SELECT * FROM user_profile WHERE id=%s",(uid,))
        result=self.cursor.fetchone()
        if result:
            data={
                "id": result[0],
                "email": result[1],
                "username": result[2],
                "phone": result[3],
                "country": result[4],
                "birthday": result[5],
                "gender": result[6],
                "user_img_url": result[7],
                "test": result[8],
                "level": result[9],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None

    def get_user_show_data(self,uid):
        self.cursor.execute("SELECT * FROM user_profile WHERE id=%s",(uid))
        result=self.cursor.fetchone()
        if result:
            data={
                "id": result[0],
                "email": result[1],
                "username": result[2],
                "level": result[7],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None

    def close(self):
        self.db.close()

########################################################################

default_app_config="user.apps.UserConfig"

print("##############################")
print("init sql user app")

# 建立個人資料table name
query(dbconfiguser,f"""
    CREATE TABLE IF NOT EXISTS `user_social` (
        `userid` VARCHAR(36) NOT NULL PRIMARY KEY,
        `email` VARCHAR(24) NOT NULL,
        `uid` VARCHAR(24) NOT NULL
    )
""") # 創建sqllogin

query(dbconfiguser,f"""
    CREATE TABLE IF NOT EXISTS `user_profile` (
        `id` VARCHAR(36) NOT NULL PRIMARY KEY,
        `email` VARCHAR(24) NOT NULL,
        `username` VARCHAR(24) NOT NULL,
        `phone` VARCHAR(16) NOT NULL,
        `country` CHAR(2),
        `birthday` DATE,
        `gender` CHAR(1),
        `user_img_url` VARCHAR(255),
        `test` TINYINT(2) UNSIGNED DEFAULT 0,
        `level` TINYINT(2) UNSIGNED DEFAULT 0
    )
""") # 創建sqluser

query(dbconfiguser,f"""
    CREATE TABLE IF NOT EXISTS `user_setting_eq`(
        `UID_EQ` VARCHAR(36) NOT NULL PRIMARY KEY,
        `ENGANCE_HIGH` BOOL,
        `ENGANCE_MIDDLE` BOOL,
        `ENGANCE_LOW` BOOL,
        `ENGANCE_HEAVY` BOOL,
        `STYLE` VARCHAR(255),
        `EQ_HIGH` INT CHECK (EQ_HIGH >=0 AND EQ_HIGH <=100),
        `EQ_MIDDLE` INT CHECK (EQ_MIDDLE >=0 AND EQ_MIDDLE <=100),
        `EQ_LOW` INT CHECK (EQ_LOW >=0 AND EQ_LOW <=100),
        `EQ_HEAVY` INT CHECK (EQ_HEAVY >=0 AND EQ_HEAVY <=100),
        `EQ_DISTORTION` INT CHECK (EQ_DISTORTION >=0 AND EQ_DISTORTION <=100),
        `EQ_ZIP` INT CHECK (EQ_ZIP >=0 AND EQ_ZIP <=100),
        `SPATIAL_AUDIO` VARCHAR(255)
    )
""") # 創建sqleq

query(dbconfiguser,f"""
    CREATE TABLE IF NOT EXISTS `user_setting`(
        `UID_SETTING` VARCHAR(36) NOT NULL PRIMARY KEY,
        `LANGUAGE` VARCHAR(255) NOT NULL,
        `SHOW_MODAL` VARCHAR(255) NOT NULL,
        `AUDIO_QUALITY` VARCHAR(255) NOT NULL,
        `AUDIO_AUTO_PLAY` BOOL NOT NULL,
        `WIFI_AUTO_DOWNLOAD` BOOL NOT NULL,
        `CREATED_AT` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""") # 創建sqlusersetting



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
    request.session["oauth_state"]=state
    url=f"https://accounts.google.com/o/oauth2/v2/auth?scope={scope}&access_type={access_type}&include_granted_scopes={include_granted_scopes}&response_type={response_type}&state={state}&redirect_uri={urlgoogle}&client_id={client_id}" # 生成 Google 登入連結
    return HttpResponseRedirect(url)

def googlecallback(request):
    success=False
    code=request.GET.get("code")
    state=request.GET.get("state")
    if code and state==request.session.get("oauth_state"):
        url="https://oauth2.googleapis.com/token"
        params={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": urlgoogle,
            "grant_type": "authorization_code"
        }
        # 向 Google API 發送 POST 請求，獲取存取令牌
        response=requests.post(url,data=params)
        token_data=response.json()
        id_token=token_data.get("id_token",None)
        access_token=token_data.get("access_token",None)

        url="https://oauth2.googleapis.com/tokeninfo"
        data={
            "id_token": id_token,
        }
        # 向 Google API 發送 GET 請求，獲取使用者資料
        response=requests.get(url,params=data)
        data=response.json()
        email=data["email"]
        picture=data["picture"]
        userid=data["sub"]
        name=data["name"]

        # 調用 base 函式進行處理
        base(userid=userid,email=email,name=name,user_img_url=picture,request=request)
        success= True
    else:
        printcolor("warning","google驗證失敗")
    request.session["isLogin"]=success
    if success:
        printcolorhaveline("green","google登入成功")
        return redirect("/music/discover/")
    else:
        printcolorhaveline("warning","google登入失敗")
        return redirect("/user/login/")

# line 登入
def lineurl(request):
    state=str(uuid.uuid4())
    # 保存 state 至 session 中，以防止 CSRF 攻擊
    request.session["oauth_state"]=state
    # 生成 Line 登入連結
    encoded_scopes=urllib.parse.quote(" ".join(scopes))
    url=f"https://access.line.me/oauth2/v2.1/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={urlline}&state={state}&scope={encoded_scopes}"
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
            "client_id": client_id,
            "client_secret": client_secret,
        }
        # 向 Line API 發送 POST 請求，獲取存取令牌
        response=requests.post(url,data)
        token_data=response.json()
        id_token=token_data.get("id_token",None)
        access_token=token_data.get("access_token",None)

        url="https://api.line.me/oauth2/v2.1/verify"
        data={
            "id_token": id_token,
            "client_id": client_id,
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

# 個人資料
def profile2(request):
    if request.method=="POST":
        # data
        id=request.session["key"]
        username=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        country=request.POST.get("country")
        birthday=request.POST.get("birthday")
        gender=request.POST.get("gender")
        userimageurl=""
        test=0
        level=0

        # 存入sql
        print("******************************")
        query(dbconfiguser,"INSERT INTO `user_profile` (`id`,`email`,`username`,`phone`,`country`,`birthday`,`gender`,`user_img_url`,`test`,`level`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id,email,username,phone,country,birthday,gender,userimageurl,test,level))
        query(dbconfiguser,"UPDATE user_profile SET email=%s,username=%s,phone=%s,country=%s,bir``thday=%s,gender=%s,user_img_url=%s,test=%s,level=%s WHERE id=%s",(email,username,phone,country,birthday,gender,userimageurl,test,level,id))

        print("成功修改")
        return redirect("/user/profile2/")
    else:
        # 查詢用戶
        uid=request.session["key"]
        row=query(dbconfiguser,"SELECT * FROM user_profile WHERE id=%s",(uid))
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
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(data)
        else:
            data=None
        return render(request,"edit_profile.html",{"form": data})


## 不知道在幹嘛的
def user_eq(request):
    if request.method=="POST":
        body=json.loads(request.body)
        kwargs=body.get("kwargs")
        printcolorhaveline("green",kwargs)
        kwargs["UID_EQ"]=request.session["key"]
        method=body.get("method")
        return JsonResponse({"data": (sqleq(dbconfiguser)).commit(method=method,kwargs=kwargs)})
    else:
        return JsonResponse({"success": False})

def user_setting(request):
    if request.method=="POST":
        body=json.loads(request.body)
        method=body.get("method")
        kwargs=body.get("kwargs")
        kwargs["UID_SETTING"]=request.session["key"]
        return JsonResponse({"data": (sqlusersetting(dbconfiguser)).commit(method=method,kwargs=kwargs)})
    else:
        return JsonResponse({"success": False})











# 註記
# 只要函式後面有加sql都是sql函式
# 話說我不知道這樣串接是否符合你們要的，有錯直接跟我說即可