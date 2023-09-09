from django.shortcuts import render
# api
from drfa.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework import status
# models1
from Reviews.models import ActivityLog
from User.models import Profile
from lib.Email.send import send_user_requset_error_mail


class CommentView(APIView):
    def get(self, request):
        print(request.GET.get("log_type"))
        return Response(ActivityLog.objects.filter(log_type=request.GET.get("log_type")).values().order_by('-created_at'))

    def post(self, request):
        try:
            porf_obj = Profile.objects.get(uid=request.data.get("uid"))
            ActivityLog.objects.create(
                profile=porf_obj, log_type=request.data.get('log_type'), content=request.data.get('content'))

            return Response({"mes": "ok"})
        except Exception as e:
            return Response({"mes": str(e)}, status=404)


# send. ================================================================


@api_view(["POST"])
def request_comments(request):
    try:
        uid = request.GET.get("uid")
        mes = request.data.get("content")
        obj = Profile.objects.get(uid=uid)
        send_user_requset_error_mail(
            who=obj.username, email=obj.email, mes=mes)

        return Response("ok")
    except Exception as e:
        return Response(str(e), status=404)


@api_view(["POST"])
def request_error_comments(request):
    try:
        uid = request.GET.get("uid")
        mes = request.data.get("content")
        obj = Profile.objects.get(uid=uid)
        send_user_requset_error_mail(
            who=obj.username, email=obj.email, mes=mes)

        return Response("ok")
    except Exception as e:
        return Response(str(e), status=404)
