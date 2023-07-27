from rest_framework import serializers
from .models import Profile, Setting, EQ, Playlist


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        exclude=['created_at']


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Setting
        exclude=['created_at']


class EQSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = EQ
        exclude = ['created_at']


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        exclude = ['created_at']
=======
        model=EQ
        exclude=['created_at']
>>>>>>> 4b657f735fae7a3dcc73711850eae71dffcef26b
