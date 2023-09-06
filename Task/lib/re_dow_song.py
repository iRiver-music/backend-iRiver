from music.models import Style, Song, FailSong, DowARtist


def re_dow_song_action(request):
    for style in Style.objects.all():
        if not Song.objects.filter(music_ID=style.music_ID).exists():
            FailSong.objects.create(
                music_ID=style.music_ID, artist=style.artist)
            # dow artist
            DowARtist.objects.create()
    pass
