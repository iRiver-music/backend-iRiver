from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from User.models import Profile, Setting, EQ, Playlist


class SettingAPIView(APIView):
    def get(self, request, uid):
        try:
            setting = Setting.objects.using("user").get(id=uid)
            data = {
                "setting": SettingSerializer(setting).data
            }
            return Response(data)
        except Setting.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid):
        try:
            setting = Setting.objects.using("user").get(id=uid)
        except Setting.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SettingSerializer(setting, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"mes": "ok"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
