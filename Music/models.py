from django.db import models
from django.utils import timezone
# Create your models here.

class Artist(models.Model):
    artist = models.CharField(max_length=255, unique=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'music'
        db_table = 'artists'

    def __str__(self):
        return self.artist

class Music(models.Model):
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    music_ID = models.CharField(max_length=255, unique=True)
    album = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    artist_url = models.CharField(max_length=255)
    sources = models.CharField(max_length=255)
    download_status = models.BooleanField(default=False)
    style = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    ch_lyrics = models.TextField()
    en_lyrics = models.TextField()
    rating = models.CharField(max_length=255)
    views = models.IntegerField()
    release_year = models.IntegerField()
    publish_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'music'
        db_table = 'songs'

    def __str__(self):
        return self.music_ID

def create_tables(ob):
    ob.objects.create_table()