from tkinter.ttk import Style
import django
from django.http import HttpRequest
from dow.views import dow_song
from lib.clear_str import process_title
from music.models import FailSong, DowARtist
import concurrent.futures

# pytube
from pytube import YouTube

from dow.views import dow_all_song
from .models import Song


def dow_fail_song_action():
    for song in FailSong.objects.all():
        try:
            url = YouTube(
                "https://www.youtube.com/watch?v={}".format(song.music_ID))

            obj = Song.objects.filter(artist=song.music_ID)
            if obj.exists():
                song.artist = obj.artist
                song.title = obj.title

            # 调用 dow_song 函数并传递参数
            dow_song_request = HttpRequest()
            dow_song_request.GET = {'title':  process_title(title=url.title, artist=url.author), "artist": song.artist,
                                    'music_ID': song.music_ID, 'artist_url': url.channel_url}

            rep = dow_song(request=dow_song_request)
            # test

            print(rep.status_code)

            if rep.status_code == 200:
                print("ok")
                FailSong.objects.filter(music_ID=song.music_ID).delete()
            elif rep.status_code == 500:
                print("error")
            else:
                print("Error")

        except Exception as e:
            pass
            # print(e)


# =================================================================


def dow_artist_action(max_workers: int):
    django.setup()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for artist in DowARtist.objects.all():
            futures.append(executor.submit(main, artist=artist))

    return True


def main(artist):
    try:
        print(artist.artist)
        dow_song_request = HttpRequest()
        dow_song_request.GET = {
            'artist': artist.artist, "artist_url": artist.artist_url, "artist_img_url": artist.artist_img_url
        }

        rep = dow_all_song(request=dow_song_request)

        if rep.status_code == 200:
            print("ok")
            DowARtist.objects.filter(artist=artist.artist).delete()

        elif rep.status_code == 500:
            print("error")
        else:
            print("Error")

    except Exception as e:
        print(e)
        # pass
