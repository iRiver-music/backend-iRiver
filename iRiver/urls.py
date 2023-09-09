"""
URL configuration for iRiver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import FileResponse
from django.conf import settings
import os


def serve_robots_txt(request):
    robots_txt_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    return FileResponse(open(robots_txt_path, 'rb'))


urlpatterns = [
    # music
    path('api/music/', include('Music.urls', namespace='Music')),
    # user
    path('api/auth/', include('User.urls', namespace='User')),
    # discover
    path('api/discover/', include('Discover.urls', namespace='Discover')),
    # ??
    path('api/token/', include('Token.urls', namespace='Token')),

    # Track  追蹤資料
    path('api/task/', include('Task.urls', namespace='Task')),

    # Track  追蹤資料
    path('api/track/', include('Track.urls', namespace='Track')),

    # Reviews 紀錄與評論
    path('api/reviews/', include('Reviews.urls', namespace='Reviews')),

    # administration
    path('api/admin/', include('Administration.urls', namespace='Administration')),



    # robots
    path('robots.txt', serve_robots_txt, name='robots_txt'),

]
