from django.conf import settings
import requests


def get_user():
    # 构建HTTP请求
    url = settings .ADMIN_URL + "/get_all_users/"

    data = {
        'username': settings.ADMIN_ACCOUNT,
        'password': settings.ADMIN_PASSWORD,
        # 添加其他数据字段
    }

    # 发送HTTP POST请求
    response = requests.post(url, data=data)

    if response.status_code == 200:
        # 请求成功，处理响应数据
        data = response.json()

        print(data)

        # return data
        # 处理数据的逻辑
    else:
        # 请求失败，处理错误
        print(f"请求失败：{response.status_code} - {response.text}")
