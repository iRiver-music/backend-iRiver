

from Music.models import FailSong, Song, Style


def check_style_song(request):
    for style in Style.objects.all():
        if not Song.objects.filter(music_ID=style.music_ID).exists() and not FailSong.objects.filter(music_ID=style.music_ID).exists():
            FailSong.objects.create(
                music_ID=style.music_ID, artist=style.artist)
    pass
