from django.middleware.csrf import get_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 這個 API 視圖負責在每次請求時生成並返回新的 CSRF token
@api_view(['GET'])
def get_csrf_token(request):
    # 使用 Django 提供的 get_token 方法生成新的 CSRF token
    new_csrf_token = get_token(request)

    # 在 Response 的 headers 中設置新的 CSRF token，讓前端可以獲取並更新
    response = Response({'csrfToken': new_csrf_token})
    response['X-CSRFToken'] = new_csrf_token
    return response

# 這個 API 視圖用於處理其他請求，你可以將它視為一個示例
@api_view(['POST'])
def some_api_endpoint(request):
    # 在這裡處理其他 POST 請求的邏輯
    # 這裡只是一個示例，你可以根據實際需求來處理 POST 請求的邏輯

    return Response({'message': 'Success'})
