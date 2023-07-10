# import
import pymysql

# self import
# none

# program START

# sql 串接
dbuser=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="django_user",charset="utf8") # user 的 db
dbmusic=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="music_db",charset="utf8") # muisc 的 db

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

def loginsql(): # 登入用sql
    pass

# 註記
# 只要函式後面有加sql都是sql函式
# 話說我不知道這樣串接是否符合你們要的，有錯直接跟我說即可