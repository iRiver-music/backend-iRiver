from django.urls import path, include

from Task.model.adminView import AdminIView
from . import views

app_name = 'Task'


urlpatterns = [
    path('', AdminIView.as_view(), name='adminView'),
]
