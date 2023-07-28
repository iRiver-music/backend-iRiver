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
                "profile": ProfileSerializer(Profile.objects.using("user").get(uid=uid)).data,
                "setting": SettingSerializer(Setting.objects.using("user").get(uid=uid)).data,
                "eq": EQSerializer(EQ.objects.using("user").get(uid=uid)).data
            }

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data)

    def post(self, request, uid):
        try:

            Profile.objects.using("user").create(
                uid=uid, username=request.data.get('username'))
            Setting.objects.using("user").create(uid=uid)
            EQ.objects.using("user").create(uid=uid)

            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "User registered {}".format(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uid):
        try:
            profile = Profile.objects.using("user").get(uid=uid)
            setting = Setting.objects.using("user").get(uid=uid)
            eq = EQ.objects.using("user").get(uid=uid)

            # Delete the related objects (Setting and EQ) first
            setting.delete(using="user")
            eq.delete(using="user")

            # Delete the Profile object
            profile.delete(using="user")

            return Response({"message": "User and related information deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
