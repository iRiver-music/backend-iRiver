# views.py
import subprocess
import json
from django.http import JsonResponse


def get_container_stats(request):
    container_name = "back-iriver"  # 替换为您的 Django 容器名称
    command = f"docker stats --no-stream --format '{{.Container}},{{.CPUPerc}},{{.MemUsage}}' {container_name}"

    try:
        output = subprocess.check_output(command, shell=True, text=True)
        container_stats = output.strip().split(',')
        container_stats_dict = {
            "container_name": container_stats[0],
            "cpu_percentage": container_stats[1],
            "memory_usage": container_stats[2]
        }
        return JsonResponse(container_stats_dict)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
