import imghdr
import os
from django.conf import settings
from pydub import AudioSegment
# pytube
from pytube import YouTube

from Music.models import Artist, FailSong, Song


def check_song_file_action():
    def fail(artist, music_ID):
        if not FailSong.objects.filter(music_ID=music_ID).exists():
            FailSong.objects.create(artist=artist, music_ID=music_ID)

    for song in Song.objects.all():
        # Define the file path
        path = os.path.join(
            settings.MEDIA_PATH, song.artist, f"{song.music_ID}.mp3")

        # Check if the file exists
        if os.path.exists(path):
            audio = AudioSegment.from_mp3(path)
            duration_seconds = len(audio) / 1000

            if duration_seconds < 30:
                os.remove(path)
                fail(song.artist, song.music_ID)
        else:
            fail(song.artist, song.music_ID)
        # download the img
        song_img_path = os.path.join(
            settings.MEDIA_PATH, "img", song.artist, f"{song.music_ID}.jpg")

        # if not os.path.exists(song_img_path):
        #     download_img(url=f"https://i.ytimg.com/vi/{song.music_ID}/hqdefault.jpg?",
        #                  file_name=f"{song.music_ID}.jpg", file_dir=f"media/{song.artist}/img/")


def check_song_artist_img_and_dow():
    for artist in Artist.objects.all():
        pass
        # if not os.path.exists(settings.MEDIA_PATH, "img", artist.artist, "artist.jpg"):
        #     download_img_base64(url=(query_artist_iocn_src(artist.artist)),
        #                         file_name='artist.jpg', file_dir=f"media/{artist.artist}/img/")
        # if not os.path.exists(settings.Base_DIR , "img" , artist.artist , "cover.jpg"):
    return True
