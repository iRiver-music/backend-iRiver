from MySQLdb import IntegrityError
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from User.serializers import SettingSerializer, ProfileSerializer, EQSerializer, PlaylistSerializer
from User.models import Profile, Setting, EQ, Playlist


class UserRegistrationAPIView(APIView):
    def post(self, request, uid):
        # Deserialize the data from the request body using the UserSerializer
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user profile to the database
            serializer.save()

            # Return a success response
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
