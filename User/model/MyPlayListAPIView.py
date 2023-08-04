from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import PlaylistSerializer
from User.models import Playlist

class MyPlayListAPIView(APIView):
    def get():
        pass