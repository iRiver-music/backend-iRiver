import MySQLdb
import json
import difflib
from Music.models import Music
from Music.models import Artist

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
    #r =self.get_all_artist()
    r = Artist.objects.all().using('test')
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
    #r = self.get_all_song(field='title')
    r = Music.objects.values('title').all().order_by('publish_time').using('test')
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


