# import
import json
import difflib
import jwt
import requests
import uuid
import urllib.parse
import pymysql
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect, render
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
dbconfigsocial=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="django_user",charset="utf8")

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

# print_color 函式：在終端機中以不同顏色打印文字
def print_color(color,text):
    # 根据传入的颜色选择相应的 ANSI 转义码
    if color == "header":
        color_code="\033[95m"
    elif color == "blue":
        color_code="\033[94m"
    elif color == "green":
        color_code="\033[92m"
    elif color == "warning":
        color_code="\033[93m"
    elif color == "fail":
        color_code="\033[91m"
    else:
        raise ValueError("Unsupported color.")

    # 打印带有颜色的文本
    print(str(color_code)+str(text)+str("\033[0m"))

# print_have_line 函式：在終端機中打印分隔線並打印文字
def print_have_line(color="green",text=""):
    print("---------------------------")
    print_color(color,text)

test=True # only for testing
url="https://iriver.ddns.net"
url="http://127.0.0.1:8000" # only for testing


# 登入
def loginsql(method,email,password,token=""):
    if method=="google":
        google()
    elif method=="line":
        line()
    elif method=="normal":
        login()
    else:
        print_have_line("fail","loginmethod error")

def google():
    pass

def line():
    pass

def login():
    pass

# 登出
def logoutsql():
    pass

# 註冊
def signupsql():
    pass








################################################################














test = True  # 測試模式的標誌，用於根據不同的環境設定相應的參數和配置
formal_url = "https://iriver.ddns.net"  # 正式環境的 URL
local_url = "http://127.0.0.1:8000"  # 本地開發環境的 URL
client_id = '1026795084542-4faa7ard63anna4utjtmavuvbe4t4mf4.apps.googleusercontent.com'
client_secret = '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'
scope = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
access_type = 'offline'
include_granted_scopes = 'true'
response_type = 'code'
client_id = '1661190797'
client_secret = '3fc12add18f596c2597c993f1f858acf'
response_type = 'code'
scopes = ["profile", "openid", "email"]

if test:
    urlgoogle=local_url + '/complete/google/'
    urlline=local_url + '/complete/line/'
else:
    urlgoogle=formal_url + '/complete/google/'
    urlline=formal_url + '/complete/line/'


########################################################################
# function START

# user/lib::
# switch_key 函式：根據鍵的格式返回對應的鍵值
def switch_key(tkey):
    if tkey.startswith('#'):
        key = tkey[1:]
    else:
        key = tkey.split("@")[0]
    return key

########################################################################

#/data/
# getdata 函式
def decode_id_token(id_token, channel_secret):
    # 將 id_token 轉換為字節類型
    id_token_bytes = id_token.encode('utf-8')
    # 解碼 id_token
    decoded = jwt.decode(id_token_bytes, channel_secret, algorithms=['HS256'], options={"verify_signature": False})
    return decoded

def get_line_user_email(access_token, channel_secret):
    # 獲取 id_token
    id_token = get_id_token(access_token)
    # 解碼 id_token 並獲取用戶郵件地址
    decoded_id_token = decode_id_token(id_token, channel_secret)
    user_email = decoded_id_token.get('email')
    return user_email

def get_id_token(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # 發送 POST 請求，驗證 id_token 並獲取驗證結果
    response = requests.post('https://api.line.me/oauth2/v2.1/verify', headers=headers)
    verify_data = response.json()
    id_token = verify_data.get('id_token')  # 獲取 id_token
    return id_token

def get_line_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # 發送 GET 請求，獲取 Line 用戶資料
    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    data = response.json()
    return data

def get_google_data(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'personFields': 'photos'}
    # 發送 GET 請求，獲取 Google 用戶資料
    response = requests.get('https://people.googleapis.com/v1/people/me', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    return None

def get_avatar_url(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'personFields': 'photos'}
    # 發送 GET 請求，獲取 Google 用戶資料
    response = requests.get('https://people.googleapis.com/v1/people/me', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            avatar_url = photos[0].get('url')  # 獲取頭像 URL
            return avatar_url
    return None

def get_user_show_data(request):
    if request.method != 'POST':
        return HttpResponse('error')
    return HttpResponse(json.dumps({
        "success": True,
        "user_data": request.session['user_data'],
        "user_playlists": request.session['user_playlist'],
    }))

# save_session 函式：保存用戶會話數據
def save_session(request,name,email,uid,userimageurl):
    request.session['key'] = uid  # 保存會話鍵
    request.session['name'] = name  # 保存用戶名
    request.session['email'] = email  # 保存郵件地址
    request.session['uid'] = uid  # 保存用戶 ID
    request.session['user_img_url'] = userimageurl  # 保存用戶頭像 URL

    # 創建 SQL 使用者實例
    sql_user = sqluser(dbconfiguser)
    # 舊版
    request.session['user_data'] = {'name': name}  # 保存用戶數據
    # 創建 SQL 音樂實例
    sql_user_music_list = sqlmusic(config=dbconfigusermusiclist, table_name=uid)
    # 創建用戶音樂列表表格（如果不存在）
    sql_user_music_list.create_tables()
    # 獲取用戶播放列表
    user_playlist = sql_user_music_list.get_playlists(isAll=True)
    request.session['user_playlist'] = user_playlist  # 保存用戶播放列表
    # eq
    user_eq = sqleq(dbconfiguser).commit(method="select", UID_EQ=uid)
    request.session['user_eq'] = user_eq  # 保存用戶均衡器設置
    # setting
    user_setting = sqlusersetting(dbconfiguser).commit(method="select", UID_SETTING=uid)
    request.session['user_setting'] = user_setting  # 保存用戶設置
    request.session.save()
    print("##############################")
    print_color("warning","save session "+str(request.session['user_data'])+str(request.session['user_playlist']))
    return JsonResponse({"success": True})

def get_user_session(request):
    uid=request.session['key']
    if request.method != 'POST':
        return HttpResponse('error')

    data = json.loads(request.body)  # 解析 JSON 數據
    get = data.get('get')  # 獲取操作類型

    if get == "user_eq":
        body = {"user_eq": request.session['user_eq']}  # 返回用戶均衡器設置
    elif get == "user_setting":
        body = {"user_setting": request.session['user_setting']}  # 返回用戶設置
    elif get == "user_show_data":
        body = {
            "user_data": request.session['user_data'],  # 返回用戶數據
            "user_playlists": request.session['user_playlist'],  # 返回用戶播放列表
            "user_img": request.session['user_img_url'],  # 返回用戶頭像 URL
        }
    elif get == "all":
        body = {
            "user_data": request.session['user_data'],  # 返回用戶數據
            "user_playlists": request.session['user_playlist'],  # 返回用戶播放列表
            "user_img_url": request.session['user_img_url'],  # 返回用戶頭像 URL
            "user_eq": request.session['user_eq'],  # 返回用戶均衡器設置
            "user_setting": request.session['user_setting'],  # 返回用戶設置
        }
    else:
        return HttpResponse('error')

    print_have_line(text=body)
    return HttpResponse(json.dumps({
        "success": True,
        "data": body
    }))

# userplaylist
def get_user_music_list(request):
    uid=request.session['key']
    PLAYLIST = "我的最愛"

    data = json.loads(request.body)  # 解析 JSON 數據
    method = data.get('method')  # 獲取操作類型

    sql_user_music_list = sqlmusic(config=dbconfigusermusiclist, table_name=uid)  # 創建 SQL 音樂實例

    if method == 'insert':
        # 插入音樂到播放列表
        return JsonResponse(json.dumps({'success': sql_user_music_list.save_data(music_ID_list=json.dumps([data.get('music_ID')], indent=4), music_list=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'get':
        # 獲取播放列表中的音樂
        return JsonResponse(list(sql_user_music_list.get_music_list(music_list=data.get('playlist', PLAYLIST))), safe=False)
    elif method == 'delete':
        # 從播放列表中刪除音樂
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_data(music_ID_list=json.dumps([data.get('music_ID')], indent=4), music_list=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'delete_playlist':
        # 刪除播放列表
        return JsonResponse(json.dumps({'success': sql_user_music_list.delete_playlist(playlist=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'create_playlist':
        # 創建播放列表
        return JsonResponse(json.dumps({'success': sql_user_music_list.create_playlist(playlist=data.get('playlist', PLAYLIST))}), safe=False)
    elif method == 'get_playlist':
        # 獲取所有播放列表
        return JsonResponse(json.dumps({'success': True, 'playlists': sql_user_music_list.get_playlists()}), safe=False)
    else:
        return JsonResponse({'success': False})

# 註冊
# none

########################################################################


# /login/
# base 函式：處理用戶登入的基本操作

# base 函式：處理用戶登入的基本操作
def base(userid, email, name, userimageurl, request):
    sql = sqllogin(dbconfiguser)
    sql_user = sqluser(dbconfiguser)

    # 檢查是否有帳號
    if sql.check_if_userid_exists(userid=userid) is None:
        uid = sql.insert(userid, email)
        sql_user.save_user_profile(id=uid,email=email,username=name,)

        # 創建用戶音樂列表表格（如果不存在）
        sqlmusic(config=dbconfigusermusiclist, table_name=uid).create_tables()

        # 註冊用戶均衡器
        sqleq(config=dbconfiguser).register(UID_EQ=uid)

        # 註冊用戶設置
        sqlusersetting(config=dbconfiguser).register(UID_SETTING=uid)
    else:
        uid = sql.insert(userid=userid, email=email)

    sql.close()

    # 保存用戶會話數據
    save_session(request,name,email,uid,userimageurl)

########################################################################

# 自製uid
def get_uuid():
    uid=uuid.uuid4()
    uid_str=str(uid).replace('-','')
    short_uid="a" + uid_str[:12]
    return short_uid

class sqlclass:
    def __init__(self,config):
        self.config=config
        self.table_name=None
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_table(self,table_name):
        print("-"*30)
        print(f"created table {table_name}")

    def commit(self,method: str,**kwargs):
        if method == "insert":
            self.insert(**kwargs)
        elif method == "update":
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

    def create_table(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                UID_EQ VARCHAR(36) NOT NULL PRIMARY KEY,
                ENGANCE_HIGH BOOL,
                ENGANCE_MIDDLE BOOL,
                ENGANCE_LOW BOOL,
                ENGANCE_HEAVY BOOL,
                STYLE VARCHAR(255),
                EQ_HIGH INT CHECK (EQ_HIGH >= 0 AND EQ_HIGH <= 100),
                EQ_MIDDLE INT CHECK (EQ_MIDDLE >= 0 AND EQ_MIDDLE <= 100),
                EQ_LOW INT CHECK (EQ_LOW >= 0 AND EQ_LOW <= 100),
                EQ_HEAVY INT CHECK (EQ_HEAVY >= 0 AND EQ_HEAVY <= 100),
                EQ_DISTORTION INT CHECK (EQ_DISTORTION >= 0 AND EQ_DISTORTION <= 100),
                EQ_ZIP INT CHECK (EQ_ZIP >= 0 AND EQ_ZIP <= 100),
                SPATIAL_AUDIO VARCHAR(255)
            )
        '''
        self.cursor.execute(sql)

        super().create_table(table_name=self.table_name)

    def commit(self,method: str,**kwargs):
        if method == "insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method == "update":
            kwargs=kwargs.get('kwargs')
            return self.update(**kwargs)
        elif method == "select":
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
        sql=f'SELECT * FROM {self.table_name} WHERE UID_EQ=%s'
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
            kwargs.get('UID_EQ'),
            kwargs.get('ENGANCE_HIGH'),
            kwargs.get('ENGANCE_MIDDLE'),
            kwargs.get('ENGANCE_LOW'),
            kwargs.get('ENGANCE_HEAVY'),
            kwargs.get('STYLE'),
            kwargs.get('EQ_HIGH'),
            kwargs.get('EQ_MIDDLE'),
            kwargs.get('EQ_LOW'),
            kwargs.get('EQ_HEAVY'),
            kwargs.get('EQ_DISTORTION'),
            kwargs.get('EQ_ZIP'),
            kwargs.get('SPATIAL_AUDIO'),
        )

    def tuple_to_dict(self,data_tuple):
        keys=[
            'UID_EQ',
            'ENGANCE_HIGH',
            'ENGANCE_MIDDLE',
            'ENGANCE_LOW',
            'ENGANCE_HEAVY',
            'STYLE',
            'EQ_HIGH',
            'EQ_MIDDLE',
            'EQ_LOW',
            'EQ_HEAVY',
            'EQ_DISTORTION',
            'EQ_ZIP',
            'SPATIAL_AUDIO'
        ]
        return dict(zip(keys,data_tuple))

    # def get_user_eq(self,UID_EQ):
    #     self.cursor.execute(
    #         'SELECT * FROM user_eq WHERE UID_EQ=%s',
    #         (UID_EQ,)
    #     )
    #     row=self.cursor.fetchone()

    #     if row:
    #         columns=[desc[0] for desc in self.cursor.description]
    #         user_eq=dict(zip(columns,row))
    #         return user_eq
    #     else:
    #         return None

class sqllogin:
    def __init__(self,config):
        self.config=config
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_tables(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS user_social (
                userid VARCHAR(36) NOT NULL PRIMARY KEY,
                email VARCHAR(24) NOT NULL,
                uid VARCHAR(24) NOT NULL
            )
        '''
        self.cursor.execute(sql)

    # 新增使用者並回傳uid
    def insert(self,userid,email):

        uid=self.check_if_email_exists(email)
        if uid is None:
            uid=get_uuid()

        if not self.check_if_userid_exists(userid):
            sql="INSERT INTO user_social (userid,email,uid) VALUES (%s,%s,%s)"
            data=(userid,email,uid)
            self.cursor.execute(sql,data)
            self.db.commit()

        return uid

    # 檢查是否有此userid
    def check_if_userid_exists(self,userid):
        sql="SELECT userid FROM user_social WHERE userid=%s"
        self.cursor.execute(sql,(userid,))
        result=self.cursor.fetchone()
        return result

    # 檢查是否有此email 回傳uid
    def check_if_email_exists(self,email):
        sql="SELECT uid FROM user_social WHERE email=%s"
        self.cursor.execute(sql,(email,))
        result=self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.db.close()

class sqlmusic:
    def __init__(self,config,table_name: str,PLAYLIST: str="我的最愛"):
        '''table'''
        self.PLAYLIST=PLAYLIST
        self.table_name=table_name
        self.config=config
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_tables(self):
        sql=f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                playlist VARCHAR(255) NOT NULL,
                music_ID VARCHAR(32) NOT NULL,
                favorite BOOLEAN NOT NULL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

    def get_music_list(self,music_list):
        sql=f'SELECT music_ID FROM {self.table_name} WHERE playlist=%s ORDER BY created_at  DESC'
        self.cursor.execute(sql,(music_list,))
        return self.cursor.fetchall()

    def save_data(self,music_ID_list,music_list):
        print(music_list)
        """1  我的最愛"""
        try:
            music_ID_list=json.loads(music_ID_list)
            for music_ID in music_ID_list:
                print("add ",music_ID," => ", music_list)
                # 查询数据库中是否已存在相同的 music_ID
                select_sql=(
                    f'SELECT COUNT(*) FROM {self.table_name} ''WHERE music_ID=%s AND playlist=%s')
                self.cursor.execute(select_sql,(music_ID,music_list))
                result=self.cursor.fetchone()
                if result[0] == 0:
                    # 不存在则插入新数据
                    insert_sql=(f'INSERT INTO {self.table_name} '
                                  '(playlist,music_ID ,favorite) '
                                  'VALUES (%s,%s ,%s)')
                    insert_values=(music_list,music_ID,False)
                    self.cursor.execute(insert_sql,insert_values)
                # 如果是我的最愛或在最愛裡面，則將favorite設為true
                if music_list == self.PLAYLIST:
                    self.set_all_favorite(music_ID,True)
                # if music_list == self.PLAYLIST or self.check_ID_in_1(music_ID) == True:
                #     self.set_all_favorite(music_ID ,True)
            # 提交事务
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete_data(self,music_ID_list,music_list: str):
        try:
            # 解析list
            music_ID_list=json.loads(music_ID_list)
            # 删除每个id
            for music_ID in music_ID_list:
                music_list_sql=(f'DELETE FROM {self.table_name} '
                                  'WHERE playlist=%s AND music_ID=%s'
                                  )
                music_list_values=(music_list,music_ID)
                self.cursor.execute(music_list_sql,music_list_values)
                # 如果是我的最愛，則將favorite設為false
                if music_list == 1:
                    self.set_all_favorite(music_ID,False)
            # 提交更改
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False

    def delete_playlist(self,playlist):
        sql=f'DELETE FROM {self.table_name} WHERE playlist=%s'
        self.cursor.execute(sql,(playlist,))
        self.db.commit()

        return True

    def chang_playlist_name(self,new_playlist_name,old_playlist_name):
        sql=f'UPDATE {self.table_name} SET playlist=%s WHERE playlist=%s'
        self.cursor.execute(sql,(new_playlist_name,old_playlist_name))
        self.db.commit()

        return True

    def setfavorite(self,music_ID_list):
        music_ID_list=json.loads(music_ID_list)
        for music_ID in music_ID_list:
            self.save_data(music_ID,1)

    def check_ID_in_1(self,music_ID):
        sql=f'SELECT * FROM {self.table_name} WHERE music_ID=%s AND playlist={self.PLAYLIST}'
        self.cursor.execute(sql,(music_ID,))
        result=self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def set_all_favorite(self,music_id,value):
        sql=f'UPDATE {self.table_name} SET favorite=%s WHERE music_ID=%s'
        self.cursor.execute(sql,(value,music_id))
        self.db.commit()

    def is_table_empty(self):
        sql=f'SELECT COUNT(*) FROM {self.table_name}'
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        count=result[0]
        return count == 0

    def get_playlists(self,isAll=False):
        if self.is_table_empty():
            return None

        sql="SELECT DISTINCT playlist FROM {}{}".format(
            self.table_name," WHERE playlist != '我的最愛'" if not isAll else "")
        self.cursor.execute(sql)
        res=self.cursor.fetchall()

        if res:
            return res
        else:
            return None

    def close(self):
        self.db.close()

class sqlsocial:
    def __init__(self,config):
        self.config=config
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def close(self):
        self.db.close()

    def get_extra_data(self,uid):
        self.cursor.execute(
            'SELECT extra_data FROM social_auth_usersocialauth WHERE uid=%s',
            (uid,)
        )
        result=self.cursor.fetchone()
        if result:
            extra_data=result[0]
            return extra_data
        else:
            return None

class sqlusersetting(sqlclass):
    def __init__(self,config):
        super().__init__(config)
        self.table_name="user_setting"

    def create_table(self):
        sql=f'''
           CREATE TABLE IF NOT EXISTS {self.table_name} (
                UID_SETTING VARCHAR(36) NOT NULL PRIMARY KEY,
                LANGUAGE VARCHAR(255) NOT NULL,
                SHOW_MODAL VARCHAR(255) NOT NULL,
                AUDIO_QUALITY VARCHAR(255) NOT NULL,
                AUDIO_AUTO_PLAY BOOL NOT NULL,
                WIFI_AUTO_DOWNLOAD BOOL NOT NULL,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

        super().create_table(table_name=self.table_name)

    def commit(self,method: str,**kwargs):
        if method == "insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method == "update":
            kwargs=kwargs.get('kwargs')
            return self.update(**kwargs)
        elif method == "select":
            return self.tuple_to_dict(data_tuple=self.select(**kwargs))
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self,**kwargs):
        sql=f'INSERT INTO {self.table_name} (UID_SETTING,LANGUAGE,SHOW_MODAL,AUDIO_QUALITY,AUDIO_AUTO_PLAY,WIFI_AUTO_DOWNLOAD) VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE UID_SETTING=UID_SETTING'
        return super().insert(sql=sql,values=self.dict_to_tuple(**1))

    def select(self,**kwargs):
        sql=f'SELECT UID_SETTING,LANGUAGE,SHOW_MODAL,AUDIO_QUALITY,AUDIO_AUTO_PLAY,WIFI_AUTO_DOWNLOAD FROM {self.table_name} WHERE UID_SETTING=%s'
        return super().select(sql=sql,values=(kwargs["UID_SETTING"],))

    def update(self,**kwargs):
        print_have_line(text=kwargs)
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
            kwargs.get('UID_SETTING'),
            kwargs.get('LANGUAGE'),
            kwargs.get('SHOW_MODAL'),
            kwargs.get('AUDIO_QUALITY'),
            kwargs.get('AUDIO_AUTO_PLAY'),
            kwargs.get('WIFI_AUTO_DOWNLOAD'),
        )

    def tuple_to_dict(self,data_tuple):
        keys=[
            'UID_SETTING',
            'LANGUAGE',
            'SHOW_MODAL',
            'AUDIO_QUALITY',
            'AUDIO_AUTO_PLAY',
            'WIFI_AUTO_DOWNLOAD'
        ]
        return dict(zip(keys,data_tuple))

class sqluser:
    def __init__(self,config):
        self.config=config
        self.connect()

    def connect(self):
        self.db=MySQLdb.connect(**self.config)
        self.cursor=self.db.cursor()

    def create_tables(self):
        sql=f'''
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
        '''
        self.cursor.execute(sql)

    def save_user_profile(self,**user_profile):
        print("*"*30)
        print(user_profile)
        id=user_profile.get('id')
        email=user_profile.get('email')
        username=user_profile.get('username')
        phone=user_profile.get('phone')
        country=user_profile.get('country')
        birthday=user_profile.get('birthday')
        gender=user_profile.get('gender')
        user_img_url=user_profile.get('user_img_url')
        test=user_profile.get('test',0)
        level=user_profile.get('level',0)
        self.cursor.execute( 'INSERT `IGNORE` INTO `user_profile` (`id`,`email`,`username`,`phone`,`country`,`birthday`,`gender`,`user_img_url`,`test`,`level`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id,email,username,phone,country,birthday,gender,user_img_url,test,level))
        self.cursor.execute('UPDATE user_profile SET email=%s,username=%s,phone=%s,country=%s,bir``thday=%s,gender=%s,user_img_url=%s,test=%s,level=%s WHERE id=%s',(email,username,phone,country,birthday,gender,user_img_url,test,level,id))
        self.db.commit()

    def get_user_data(self,uid):
        self.cursor.execute('SELECT * FROM user_profile WHERE id=%s',(uid,))
        result=self.cursor.fetchone()
        if result:
            data={
                'id': result[0],
                'email': result[1],
                'username': result[2],
                'phone': result[3],
                'country': result[4],
                'birthday': result[5],
                'gender': result[6],
                'user_img_url': result[7],
                'test': result[8],
                'level': result[9],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None

    def get_user_show_data(self,uid):
        self.cursor.execute('SELECT * FROM user_profile WHERE id=%s',(uid))
        result=self.cursor.fetchone()
        if result:
            data={
                'id': result[0],
                'email': result[1],
                'username': result[2],
                'level': result[7],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None

    def close(self):
        self.db.close()


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



########################################################################

default_app_config='user.apps.UserConfig'

print("#"*30)
print("init sql user app")

# 建立個人資料table name
sqllogin(config=dbconfiguser).create_tables()
sql_user=sqluser(config=dbconfiguser)
sql_user.create_tables()
sqleq(config=dbconfiguser).create_table()
sqlusersetting(config=dbconfiguser).create_table()







def usersave_session(request):
    return save_session(request,request.session['name'],request.session['email'],request.session['key'],request.session['user_img_url'])


# def userget_user_music_list(request):
#     return get_user_music_list(request,request.session['key'])


# 舊款
def userget_user_show_data(request):
    return get_user_show_data(request)


# def userget_user_session(request):
#     return get_user_session(request,request.session['key'])


def check_login(request):
    if request.session["isLogin"]:
        return JsonResponse({'isLogin': request.session['isLogin']})
    else:
        return JsonResponse({'isLogin': False})

# google 登入
def googleurl(request):
    state = str(uuid.uuid4()) # 保存 state 至 session 中，以防止 CSRF 攻擊
    request.session['oauth_state'] = state
    url = f'https://accounts.google.com/o/oauth2/v2/auth?scope={scope}&access_type={access_type}&include_granted_scopes={include_granted_scopes}&response_type={response_type}&state={state}&redirect_uri={urlgoogle}&client_id={client_id}' # 生成 Google 登入連結
    return HttpResponseRedirect(url)

def googlecallback(request):
    success =  False
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state == request.session.get('oauth_state'):
        url = 'https://oauth2.googleapis.com/token'
        params = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': urlgoogle,
            'grant_type': 'authorization_code'
        }
        # 向 Google API 發送 POST 請求，獲取存取令牌
        response = requests.post(url, data=params)
        token_data = response.json()
        id_token = token_data.get('id_token', None)
        access_token = token_data.get('access_token', None)

        url = 'https://oauth2.googleapis.com/tokeninfo'
        data = {
            'id_token': id_token,
        }
        # 向 Google API 發送 GET 請求，獲取使用者資料
        response = requests.get(url, params=data)
        data = response.json()
        email = data['email']
        picture = data['picture']
        userid = data['sub']
        name = data['name']

        # 調用 base 函式進行處理
        base(userid=userid, email=email, name=name, user_img_url=picture, request=request)
        success =  True
    else:
        print("驗證失敗")
    request.session['isLogin'] = success
    if success:
        print_have_line(text="登入成功")
        return redirect('/music/discover/')
    else:
        print_have_line(text="登入失敗")
        return redirect('/user/login/')

# line 登入
def lineurl(request):
    state = str(uuid.uuid4())
    # 保存 state 至 session 中，以防止 CSRF 攻擊
    request.session['oauth_state'] = state
    # 生成 Line 登入連結
    encoded_scopes = urllib.parse.quote(" ".join(scopes))
    url = f'https://access.line.me/oauth2/v2.1/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={urlline}&state={state}&scope={encoded_scopes}'
    return HttpResponseRedirect(url)

def linecallback(request):
    success = False
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state == request.session.get('oauth_state'):
        url = 'https://api.line.me/oauth2/v2.1/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': urlline,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        # 向 Line API 發送 POST 請求，獲取存取令牌
        response = requests.post(url, data)
        token_data = response.json()
        id_token = token_data.get('id_token', None)
        access_token = token_data.get('access_token', None)

        url = 'https://api.line.me/oauth2/v2.1/verify'
        data = {
            'id_token': id_token,
            'client_id': client_id,
        }
        # 向 Line API 發送 POST 請求，獲取用戶資料
        response = requests.post(url, data=data)
        data = response.json()
        email = data['email']
        picture = data['picture']
        userid = data['sub']
        name = data['name']

        # 調用 base 函式進行處理
        base(userid, email, name, picture, request)
        success =  True
    else:
        print("驗證失敗")

    request.session['isLogin'] = success
    if success:
        print_have_line(text="登入成功")
        return redirect('/music/discover/')
    else:
        print_have_line(text="登入失敗")
        return redirect('/user/login/')

# 個人資料
def profile2(request):
    sql = sqluser(dbconfiguser)
    if request.method == 'POST':
        form_data = {
            'id': request.session['key'],
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'country': request.POST.get('country'),
            'birthday': request.POST.get('birthday'),
            'gender': request.POST.get('gender'),
        }
        sql.save_user_profile(**form_data)
        print("成功修改")
        return redirect('/user/profile2/')
    else:
        old_data = sql.get_user_data(uid=request.session['key'])
        return render(request, 'edit_profile.html', {'form': old_data})


def user_eq(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        kwargs = body.get("kwargs")
        print_have_line(text=kwargs)
        kwargs['UID_EQ'] = request.session['key']
        return JsonResponse({"data": (sqleq(dbconfiguser)).commit(method=body.get("method"), kwargs=kwargs)})
    else:
        return JsonResponse({"success": False})


def user_setting(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        method = body.get("method")
        kwargs = body.get("kwargs")
        kwargs['UID_SETTING'] = request.session['key']
        return JsonResponse({"data": (sqlusersetting(dbconfiguser)).commit(method=method, kwargs=kwargs)})
    else:
        return JsonResponse({"success": False})













# 註記
# 只要函式後面有加sql都是sql函式
# 話說我不知道這樣串接是否符合你們要的，有錯直接跟我說即可