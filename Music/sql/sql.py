import MySQLdb
import json
import difflib
from Music.models import Music
from Music.models import Artist
class SQL: 
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def get_style(self, music_ID):
        try:
            song = Music.objects.get(music_ID=music_ID)
            if song.style:
                return song.style
            else:
                return "null"
        except Music.DoesNotExist:
            return "null"
        except Exception as e:
            print(f"get_style error: {e}")
            return "null"

    def get_all_song(self, field='*'):
        try:
            if field == '*':
                # 如果 field 是 '*'，則返回所有欄位的資料
                songs = Music.objects.all().order_by('publish_time')
            else:
                # 否則，返回指定欄位的資料
                songs = Music.objects.values(field).all().order_by('publish_time')

            return list(songs)
        except Exception as e:
            print(f"get_all_song error: {e}")
            return []

    def get_all_artist(self):
        get_artists = Artist.objects.all()
        return list(get_artists)

    def get_all_artist_song(self, artist):
        try: 
            artists_songs = Music.objects.filter(artist).order_by('views')
            music_list_infos = []
            for song in artists_songs :
                music_list_infos.append(
                    {
                        'artist': song.artist,
                        'title': song.title,
                        'music_ID': song.music_ID,
                        'artist_url': song.artist_url,
                        'keywords': song.keywords,
                        'views': song.views,
                        'publish_time': song.publish_time
                    }
                )
            return music_list_infos
        except Exception as e:
            print(f"get_all_artist_song error: {e}")
            return None

    def get_artist_summary(self, artist: str) -> str:
        artist = artist.strip()
        try:
            artist = Artist.objects.get(artist=artist)
            return artist.summary
        except Artist.DoesNotExist:
            print(f"no summary")
            return None
        
    def query(self, query):
        artist_song_res , artist_song_sorce = self.query_all_artist_song(artist=query) or (None,0)
        song_res        , song_score = self.query_song(song_name=query) or (None, 0)
        
        if(artist_song_sorce > song_score):
            forwards = artist_song_res
            back = song_res
        else:
            forwards = song_res
            back = artist_song_res
        
        result = []
        if forwards is not None:
            result.extend(forwards)
        if back is not None:
            result.extend(back)

        return tuple(result)

    def query_all_artist_song(self, artist):
        r =self.get_all_artist()
        try :
            matches = difflib.get_close_matches(artist, [x[1] for x in r], n=3, cutoff=0.4)
            score = difflib.SequenceMatcher(None, artist, matches[0]).ratio()
        except Exception as e:
            # print(e)
            return None , 0
        if matches is None:
            return None , 0
        result = Music.objects.filter(artist__in=matches).order_by('-views')[:4]
        return result, score
    
    def query_song(self , song_name):
        r = self.get_all_song(field='title')
        try:
            matches = difflib.get_close_matches(song_name, [x[0] for x in r],n= 3, cutoff=0.0003)
            score = difflib.SequenceMatcher(None, song_name, matches[0]).ratio()
            # print('*'*20)
            # print(f'get_song sorce{score}')
        except Exception as e:
            print(e)
            return None ,0
        if not matches:
            return None ,0
        result = Music.objects.filter(title__in=matches).order_by('-views')[:4]
        return result, score
    
    def get_music_list_infos(self, music_ID_list):
        try:
            music_list_infos = [] 
            for music_ID in music_ID_list:
                music = Music.objects.get(music_ID_list)
                if music != None:
                    music_list_infos.append(
                        {
                            'artist': music.artist,
                            'title': music.title,
                            'music_ID': music.music_ID,
                            'artist_url': music.artist_url,
                            'keywords': music.keywords,
                            'views': music.views,
                            'publish_time': music.publish_time
                        }
                    )
            return music_list_infos
        except Exception as e:
            print(f"get_music_list_infos error: {e}")
            return None

