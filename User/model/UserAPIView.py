from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.models import Setting, EQ, Profile
from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer
# firebase
from User.Authentication.authentication import FirebaseAuthentication

#  ----------------------------------------------------------------


class UserAPIView(APIView):
    # authentication_firebase
    authentication_classes = [FirebaseAuthentication]

    # 取得帳號資料
    def get(self, request, uid):
        try:
            data = {
                "profile": ProfileSerializer(Profile.objects.get(uid=uid)).data,
                "setting": SettingSerializer(Setting.objects.get(uid=uid)).data,
                "eq": EQSerializer(EQ.objects.get(uid=uid)).data
            }

            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # 註冊
    def post(self, request, uid):
        # 檢查是否邀請碼正確
        try:
            if not Profile.objects.filter(invitation_code=request.data["invited_by_code"]).exists():
                return Response({"mes": "error invited_by_code"}, status=status.HTTP_404_NOT_FOUND)

            if Profile.objects.filter(uid=uid).exists():
                return Response({"mes": "uid exists"}, status=status.HTTP_404_NOT_FOUND)

            Profile.objects.create(
                **request.data)
            Setting.objects.create(uid=uid)
            EQ.objects.create(uid=uid)

            data = {
                "profile": ProfileSerializer(Profile.objects.get(uid=uid)).data,
                "setting": SettingSerializer(Setting.objects.get(uid=uid)).data,
                "eq": EQSerializer(EQ.objects.get(uid=uid)).data
            }

            return Response(data)

        except Exception as e:
            return Response({"mes": str(e)}, status=status.HTTP_404_NOT_FOUND)
