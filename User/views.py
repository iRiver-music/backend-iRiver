from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer
from .models import Profile, Setting, EQ

# get all user data

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
            return Response({"message": "Profile updated successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SettingAPIView(APIView):
    def get(self, request, uid):
        try:
            data = {
                "setting": SettingSerializer(Setting.objects.using("user").get(id=uid)).data,
            }

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data)


class EQAPIView(APIView):
    def get(self, request, uid):
        try:
            data = {
                "eq": EQSerializer(EQ.objects.using("user").get(id=uid)).data
            }

        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data)


class UserRegistrationAPIView(APIView):
    def post(self, request, uid):
        # Deserialize the data from the request body using the UserSerializer
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user profile to the database
            serializer.save()

            # Return a success response
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
