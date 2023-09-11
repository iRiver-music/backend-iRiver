from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from User.serializers import PlaylistSerializer
from User.models import Playlist
from Music.models import Song
from Music.serializers import SongSerializer

# rate
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator


def get_uid_fav_song(uid: str) -> list:
    obj = Playlist.objects.filter(uid=uid, playlist="fav").values()
    music_info_list = []

    for item in obj:
        try:
            music = Song.objects.get(music_ID=item["music_ID"])
            music_info = SongSerializer(music).data
            music_info_list.append(music_info)
        except:
            pass

    return music_info_list


@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='GET'), name='get')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='POST'), name='post')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='PUT'), name='put')
@method_decorator(ratelimit(key='ip', rate=settings.RATELIMITS_USER, method='DELETE'), name='delete')
class PlaylistAPIView(APIView):
    def get(self, request, uid, playlist=None):
        if playlist is None:
            try:
                return Response(get_uid_fav_song(uid=uid))

            except Exception as e:
                return Response({"mes": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj = Playlist.objects.filter(uid=uid, playlist=playlist).values()

            music_info_list = []

            for item in obj:
                try:
                    music = Song.objects.get(music_ID=item["music_ID"])
                    music_info = SongSerializer(music).data
                    music_info_list.append(music_info)
                except Song.DoesNotExist:
                    return Response({"mes": "song not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response(music_info_list)

    @ratelimit(key='user', rate='user')
    def post(self, request, uid, playlist=None):
        # Access the data from the request data directly
        playlist_data = request.data

        # Check if the 'music_ID' already exists in the same playlist
        if playlist is None and not Playlist.objects.filter(uid=uid, playlist="fav", music_ID=playlist_data["music_ID"]).exists():
            try:
                existing_playlist = Playlist.objects.create(
                    uid=uid, playlist="fav", music_ID=playlist_data['music_ID'], favorite=True)
                return Response({"mes": "OK"}, status=status.HTTP_200_OK)
            except Playlist.DoesNotExist:
                return Response({"mes": "palylist error."}, status=status.HTTP_404_NOT_FOUND)
        try:
            if playlist:
                playlist = Playlist(uid=uid, ** playlist_data)
                # Save the playlist object to the specified database
                playlist.save()
                return Response({"mes": "Playlist uploaded successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"mes": "Failed to create playlist"}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            return Response({"mes": "Failed to create playlist. Validation error: {}".format(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"mes": "Failed to create playlist. The 'id' field may already exist."}, status=status.HTTP_400_BAD_REQUEST)

    @ratelimit(key='user', rate='user')
    def put(self, request, uid, playlist):
        try:
            playlists = Playlist.objects.filter(playlist=playlist, uid=uid)
        except Playlist.DoesNotExist:
            return Response({"mes": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({"mes": "Playlist updated successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"mes": "Failed to update playlist"}, status=status.HTTP_400_BAD_REQUEST)

    @ratelimit(key='user', rate='user')
    def delete(self, request, uid, playlist=None):
        if len(request.data) == 0:
            # 刪除我的最愛
            try:
                if playlist is None:
                    Playlist.objects.filter(uid=uid, playlist="fav").delete()
                    return Response({"mes": "Playlist deleted successfully"})
                else:
                    Playlist.objects.filter(uid=uid,
                                            playlist=playlist).delete()
                    return Response({"mes": "Playlist deleted successfully"})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                if playlist is None:
                    Playlist.objects.filter(
                        uid=uid, playlist="fav", music_ID=request.data["music_ID"]).delete()
                    return Response({"mes": "Playlist deleted successfully"})
                else:
                    Playlist.objects.get(uid=uid,
                                         playlist=playlist, music_ID=request.data["music_ID"]).delete()
                    return Response({"mes": "Playlist deleted successfully"})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
