from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.models import Setting,EQ,Profile
from User.serializers import SettingSerializer,ProfileSerializer,EQSerializer


class UserAPIView(APIView):
    # 取得帳號資料
    def get(self,request,uid):
        try:
            data={
                "profile": ProfileSerializer(Profile.objects.get(uid=uid)).data,
                "setting": SettingSerializer(Setting.objects.get(uid=uid)).data,
                "eq": EQSerializer(EQ.objects.get(uid=uid)).data
            }
            return Response(data)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

    # 註冊?
    def post(self,request,uid):
        try:
            Profile.objects.create(uid=uid,username=request.data.get('username'))
            Setting.objects.create(uid=uid)
            EQ.objects.create(uid=uid)

            return Response({"message": "User registered successfully"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "User registered {}".format(e)},status=status.HTTP_404_NOT_FOUND)

    # 刪除帳號
    def delete(self,request,uid):
        try:
            # 刪除物件
            Setting.objects.get(uid=uid).delete()
            EQ.objects.get(uid=uid).delete()
            Profile.objects.get(uid=uid).delete()
            return Response({"message": "User and related information deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)
