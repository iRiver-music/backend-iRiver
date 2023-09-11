from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer
from User.models import Setting

# rate
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='GET'), name='get')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='POST'), name='post')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='PUT'), name='put')
class SettingAPIView(APIView):
    def get(self, request, uid):
        try:
            setting = Setting.objects.get(uid=uid)
            data = {
                "setting": SettingSerializer(setting).data
            }
            return Response(data)
        except Setting.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @ratelimit(key='user', rate='user')
    def post(self, request, uid):
        pass

    @ratelimit(key='user', rate='user')
    def put(self, request, uid):
        try:
            setting = Setting.objects.get(uid=uid)
        except Setting.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        # 使用 request.data 中的欄位動態更新 EQ Model 的資料
        for key, value in request.data.items():
            setattr(setting, key, value)
        try:
            setting.save()
            return Response({"message": "setting updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to update setting"}, status=status.HTTP_400_BAD_REQUEST)
