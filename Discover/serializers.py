from rest_framework import serializers

from Music.models import StyleTitle
from .models import DiscoverTitle


class DiscoverTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscoverTitle
        fields = '__all__'


class StyleTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleTitle
        exclude = ['created_at']
