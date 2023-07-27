from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.models import Setting, EQ, Profile

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer


class UserAPIView(APIView):
    def get(self, request, uid):
        try:
            data = {
                "profile": ProfileSerializer(Profile.objects.using("user").get(id=uid)).data,
                "setting": SettingSerializer(Setting.objects.using("user").get(id=uid)).data,
                "eq": EQSerializer(EQ.objects.using("user").get(id=uid)).data
            }

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data)
