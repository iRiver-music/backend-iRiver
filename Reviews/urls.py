from django.urls import path, include

from . import views

app_name = 'Reviews'


urlpatterns = [
    path('comment', views.CommentView.as_view(), name=""),


    path('comment/send', views.request_comments, name="request_comments"),
    path('error/send', views.request_error_comments,
         name="request_error_comments"),
]
