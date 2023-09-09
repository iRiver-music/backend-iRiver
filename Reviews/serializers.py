from rest_framework import serializers

from Task.models import TaskLog


class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = '__all__'
