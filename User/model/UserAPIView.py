from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Track.views import device_view

from User.models import Setting, EQ, Profile
from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer
# firebase
from User.Authentication.authentication import FirebaseAuthentication
from User.views import contract

# rate
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

#  ----------------------------------------------------------------


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='GET'), name='get')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='POST'), name='post')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='DELETE'), name='delete')
class UserAPIView(APIView):
    # authentication_firebase
    authentication_classes = [FirebaseAuthentication]

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

            # 註冊時紀錄帳號裝置
            device_view(request=request)

            # 合約
            contract(request=request, uid=uid)

            return Response(data)

        except Exception as e:
            return Response({"mes": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uid):
        try:
            Profile.objects.filter(
                uid=uid).delete()
            Setting.objects.filter(uid=uid).delete()
            EQ.objects.filter(uid=uid).delete()

            # response
            return Response("ok")
        except Exception as e:
            print(e)
        return Response({"mes": str(e)}, status=status.HTTP_404_NOT_FOUND)
