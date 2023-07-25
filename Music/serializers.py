from rest_framework import serializers
from .models import Song, Album, Artist


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        exclude = ['created_at']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ['created_at']
