from rest_framework import serializers
from .models import Profile, Setting, EQ


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['created_at']


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        exclude = ['created_at']


class EQSerializer(serializers.ModelSerializer):
    class Meta:
        model = EQ
        exclude = ['created_at']
