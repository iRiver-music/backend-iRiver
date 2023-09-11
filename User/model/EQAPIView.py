from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import EQSerializer
from User.models import EQ
# rate
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='GET'), name='get')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='POST'), name='post')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='PUT'), name='put')
class EQAPIView(APIView):
    def get(self, request, uid):
        try:
            eq = EQ.objects.get(uid=uid)
            return Response({"eq": EQSerializer(eq).data})
        except EQ.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        pass

    def put(self, request, uid):
        try:
            eq = EQ.objects.get(uid=uid)
        except EQ.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 使用 request.data 中的欄位動態更新 EQ Model 的資料
        for key, value in request.data.items():
            setattr(eq, key, value)

        try:
            eq.save()  # 儲存更新後的資料至指定的資料庫
            return Response({"message": "EQ updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to update EQ"}, status=status.HTTP_400_BAD_REQUEST)
