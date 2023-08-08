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
    # authentication_classes = [FirebaseAuthentication]

    # 取得帳號資料
    def get(self,request,uid):
        try:
            data = {
                "profile": ProfileSerializer(Profile.objects.using("user").get(uid=uid)).data,
                "setting": SettingSerializer(Setting.objects.using("user").get(uid=uid)).data,
                "eq": EQSerializer(EQ.objects.using("user").get(uid=uid)).data
            }

            return Response(data)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # 註冊
    def post(self, request, uid):
        # 使用新的序列化器来验证和处理请求数据
        serializer = self.CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not Profile.objects.filter(uid=uid).exists():
                    Profile.objects.create(
                        uid=uid, username=serializer.validated_data['username'])
                if not Setting.objects.filter(uid=uid).exists():
                    Setting.objects.create(uid=uid)
                if not EQ.objects.filter(uid=uid).exists():
                    EQ.objects.create(uid=uid)

                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"message": "User registered {}".format(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
