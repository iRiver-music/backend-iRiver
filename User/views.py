from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from .models import Profile, Setting, EQ, Playlist

# get all user data


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


# handle request with EQ


class EQAPIView(APIView):
    def get(self, request, uid):
        try:
            eq = EQ.objects.using("user").get(id=uid)
            serializer = EQSerializer(eq)
            return Response(serializer.data)
        except EQ.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid):
        try:
            eq = EQ.objects.using("user").get(id=uid)
        except EQ.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # 使用 request.data 中的欄位動態更新 EQ Model 的資料
        for key, value in request.data.items():
            setattr(eq, key, value)

        try:
            eq.save(using="user")  # 儲存更新後的資料至指定的資料庫
            return Response({"message": "EQ updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to update EQ"}, status=status.HTTP_400_BAD_REQUEST)

# handle request with playlist


class PlaylistAPIView(APIView):
    def get(self, request, uid, playlist=None):
        if playlist is None:
            playlists = Playlist.objects.using("user").all()
            serializer = PlaylistSerializer(playlists, many=True)
            return Response(serializer.data)
        else:
            try:
                playlist = Playlist.objects.using(
                    "user").get(playlist=playlist)
                serializer = PlaylistSerializer(playlist)
                return Response(serializer.data)
            except Playlist.DoesNotExist:
                return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid, playlist=None):
        try:
            playlists = Playlist.objects.using(
                "user").filter(playlist=playlist, uid=uid)
        except Playlist.DoesNotExist:
            return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

        # Access the data from the request data directly
        playlist_data = request.data

        # Update each playlist object with the new data
        for playlist in playlists:
            for key, value in playlist_data.items():
                setattr(playlist, key, value)

        try:
            # Save the updated data to the specified database
            for playlist in playlists:
                playlist.save(using="user")
            return Response({"message": "Playlist updated successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Failed to update playlist"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uid, playlist=None):
        # Access the data from the request data directly
        playlist_data = request.data

        # Check if the 'music_ID' already exists in the same playlist
        if playlist is not None:
            try:
                existing_playlist = Playlist.objects.using('user').get(
                    uid=uid, playlist=playlist, music_ID=playlist_data['music_ID'])
                return Response({"error": "Playlist with the same 'music_ID' already exists in the same playlist"}, status=status.HTTP_400_BAD_REQUEST)
            except Playlist.DoesNotExist:
                pass

        try:
            playlist = Playlist(**playlist_data)

            # Save the playlist object to the specified database
            playlist.save(using='user')
            return Response({"message": "Playlist uploaded successfully"}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"error": "Failed to create playlist. Validation error: {}".format(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Failed to create playlist. The 'id' field may already exist."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, playlist=None):
        if playlist is not None:
            playlist = Playlist.objects.using(
                "user").get(id=uid, playlist=playlist)
            playlist.delete()
        else:
            try:
                playlist = Playlist.objects.using("user").get(
                    playlist=request.data["playlist"], music_ID=request.data["music_ID"])
                playlist.delete()
                return Response({"message": "Playlist deleted successfully"})
            except Playlist.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


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
