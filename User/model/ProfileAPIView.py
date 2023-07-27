from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from User.models import Profile, Setting, EQ, Playlist


class ProfileAPIView(APIView):
    def get(self, request, uid):
        try:
            profile = Profile.objects.using("user").get(id=uid)
            data = {
                "profile": ProfileSerializer(profile).data,
            }
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data)

    def put(self, request, uid):
        try:
            profile = Profile.objects.using("user").get(id=uid)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 使用 ProfileSerializer 反序列化請求的資料
        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()  # 儲存更新後的資料至資料庫
            return Response({"mes": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
