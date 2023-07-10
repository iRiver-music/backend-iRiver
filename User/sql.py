# import
import pymysql

# self import
# none

# program START

# sql 串接
dbuser=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="django_user",charset="utf8") # user 的 db
dbmusic=pymysql.connect(host="iriversql.ddns.net",port=3306,user="gWvPZkyaanAP5cXQqE8hkX5hnmYYhcMr",passwd="JABmQsQhpj05F6WI",db="music_db",charset="utf8") # muisc 的 db

query=dbuser.cursor() # 操作游標

def loginsql(): # 登入用sql def
    pass

try:
    query.execute("INSERT INTO `sqltest`(`test`,`test2`,`test3`)VALUES(%s,%s,%s)",("123","234","345")) # 執行語法
    dbuser.commit() # 提交修改
    print("success")
except Exception as e:
    # 發生錯誤時停止執行SQL
    dbuser.rollback()
    print("[ERROR]"+str(e))

# 關閉連線
dbuser.close()


# 註記
# 只要函式後面有加sql都是sql函式
# 話說我不知道這樣串接是否符合你們要的，有錯直接跟我說即可