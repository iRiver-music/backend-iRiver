from rest_framework import serializers
from .models import Music, Artist


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        exclude = ['created_at']

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        exclude = ['created_at']