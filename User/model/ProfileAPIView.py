from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import ProfileSerializer
from User.models import Profile


class ProfileAPIView(APIView):
    def get(self,request,uid):
        try:
            profile=Profile.objects.get(uid=uid)
            data={
                "profile": ProfileSerializer(profile).data,
            }
        except Profile.DoesNotExist:
            return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

        return Response(data)

    def post(self,request,uid):
        pass

    def put(self,request,uid):
        try:
            profile=Profile.objects.get(uid=uid)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)

        # 使用 request.data 中的欄位動態更新 EQ Model 的資料
        for key,value in request.data.items():
            setattr(profile,key,value)

        try:
            profile.save()  #
            return Response({"message": "profile updated successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to update profile"},status=status.HTTP_400_BAD_REQUEST)
