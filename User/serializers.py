from rest_framework import serializers
from .models import Profile, Setting, EQ, Playlist, AdminCount, LastUsersong

# 轉成json格式(捨棄`created_at`字段)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["created_at"]


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        exclude = ["created_at"]


class EQSerializer(serializers.ModelSerializer):
    class Meta:
        model = EQ
        exclude = ["created_at"]


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        exclude = ["created_at"]


class PlaylistSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["playlist"]


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCount
        exclude = ["created_at"]


class LastUsersongSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastUsersong
        exclude = ["created_at", "uid"]
