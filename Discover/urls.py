from django.urls import path, include
from . import views

app_name = 'Discover'

urlpatterns = [
    path('creat/',
         views.push_discover, name='creat'),

    path('edit/',
         views.DiscoverEditView.as_view(), name='DiscoverEditView'),
    # last
    path('<str:uid>/',
         views.discover, name='discover'),

]
