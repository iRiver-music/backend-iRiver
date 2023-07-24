import MySQLdb
import json
import difflib
from .models import Music
from .models import Artist
from .serializers import ArtistSerializer
from .serializers import MusicSerializer

def query(query):
    artist_song_res , artist_song_sorce = query_all_artist_song(artist=query) or (None,0)
    song_res        , song_score = query_song(song_name=query) or (None, 0)
    #print(artist_song_res, artist_song_sorce)
    #print(song_res, song_score)
    
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
    #print('result : ', result)
    return result

def query_all_artist_song(artist):
    #r =self.get_all_artist()
    r = list(Artist.objects.all().using('test'))
    #print(r)

    try :
        #print('inside')
        matches = difflib.get_close_matches(artist, [x.artist for x in r], n=3, cutoff=0.4)
        #print("matches:")
        #print(matches)
        score = difflib.SequenceMatcher(None, artist, matches[0]).ratio()
        #print("score:", score)
    except Exception as e:
        print("ERROR in query_all_artist_song at query.py")
        print(e)
        return None , 0
    if matches is None:
        print('match is none')
        return None , 0
    result = Music.objects.using('test').filter(artist__in=matches).order_by('-views')[:4]
    #print("result:", result)
    # result -> QureySet
    return result, score

def query_song(song_name):
    #r = self.get_all_song(field='title')
    r = list(Music.objects.using('test').values('title').all().order_by('publish_time'))
    #print('music:', r)

    try:
        matches = difflib.get_close_matches(song_name, [x['title'] for x in r],n = 3, cutoff=0.0003)
        #print("matches", matches)
        score = difflib.SequenceMatcher(None, song_name, matches[0]).ratio()
        # print('*'*20)
        # print(f'get_song sorce{score}')
    except Exception as e:
        print("ERROR in query_song at query.py")
        print(e)
        return None ,0
    if not matches:
        return None ,0
    result = Music.objects.using('test').filter(title__in=matches).order_by('-views')[:4]
    #print('query_song : ', result)
    #print('query_song : ', score)
    return result, score


