from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from User.models import Profile, Setting, EQ, Playlist


class PlaylistAPIView(APIView):
    def get(self, request, uid, playlist=None):
        print(uid)
        if playlist is None:
            playlists = Playlist.objects.filter(uid=uid)
            serializer = PlaylistSerializer(playlists, many=True)
            return Response(serializer.data)
        else:
            try:
                playlist = Playlist.objects.get(playlist=playlist)
                serializer = PlaylistSerializer(playlist)
                return Response(serializer.data)
            except Playlist.DoesNotExist:
                return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uid, playlist=None):
        try:
            playlists = Playlist.objects.filter(playlist=playlist, uid=uid)
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
                playlist.save()
            return Response({"message": "Playlist updated successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Failed to update playlist"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uid, playlist=None):
        # Access the data from the request data directly
        playlist_data = request.data

        # Check if the 'music_ID' already exists in the same playlist
        if playlist is not None:
            try:
                existing_playlist = Playlist.objects.get(
                    uid=uid, playlist=playlist, music_ID=playlist_data['music_ID'])
                return Response({"error": "Playlist with the same 'music_ID' already exists in the same playlist"}, status=status.HTTP_400_BAD_REQUEST)
            except Playlist.DoesNotExist:
                pass

        try:
            playlist = Playlist(**playlist_data)

            # Save the playlist object to the specified database
            playlist.save()
            return Response({"message": "Playlist uploaded successfully"}, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            return Response({"error": "Failed to create playlist. Validation error: {}".format(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Failed to create playlist. The 'id' field may already exist."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, playlist=None):
        if playlist is not None:
            playlist = Playlist.objects.get(id=uid, playlist=playlist)
            playlist.delete()
        else:
            try:
                playlist = Playlist.objects.get(
                    playlist=request.data["playlist"], music_ID=request.data["music_ID"])
                playlist.delete()
                return Response({"message": "Playlist deleted successfully"})
            except Playlist.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
