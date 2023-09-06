from Music.models import Artist, DowARtist, Song

import concurrent.futures

from Task.lib.playlist import get_all_playlists_music_ID_with_retry


def update_song_action(max_workers: int):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for artist in Artist.objects.all():
            futures.append(executor.submit(run, artist=artist))

    return True


def run(artist: Artist):
    try:
        song_count = len(Song.objects.filter(artist=artist))

        new_song_count = len(
            get_all_playlists_music_ID_with_retry(url=artist.artist_url))

        if song_count != new_song_count and not DowARtist.objects.filter(artist=artist.artist).exists():
            DowARtist.objects.create(
                artist=artist, artist_url=artist.artist_url, artist_img_url=artist.artist_img_url)
    except Exception as e:
        print(e)
        pass
