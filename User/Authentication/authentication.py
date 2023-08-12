
import firebase_admin
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


#  ----------------------------------------------------------------


# firebase
cred = credentials.Certificate(
    "iRiver/iside-bf18c-firebase-adminsdk-o5z7t-8ccbc22def.json")
firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization")

        if header and header.startswith("Bearer "):
            token = header.replace("Bearer ", "")

            try:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token["uid"]
                email = decoded_token["email"]
                print(email)

                # 返回驗證成功的用戶
                return (uid, None)
            except Exception as e:
                raise AuthenticationFailed(str(e))

        return None
