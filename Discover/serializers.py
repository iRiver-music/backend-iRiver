from rest_framework import serializers
from .models import DiscoverTitle


class DiscoverTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscoverTitle
        fields = '__all__'
