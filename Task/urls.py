from django.urls import path, include

from . import views

app_name = 'Task'


urlpatterns = [

    path('test', views.test, name="test"),
    path('init', views.initialize, name="init"),
    path('log', views.get_task_log, name="log"),
    path('lib', views.LibraryView.as_view(), name="lib"),

]
