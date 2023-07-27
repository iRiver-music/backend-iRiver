import time

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

# switch_key 函式：根據鍵的格式返回對應的鍵值
def switch_key(tkey):
    if tkey.startswith("#"):
        key=tkey[1:]
    else:
        key=tkey.split("@")[0]
    return key