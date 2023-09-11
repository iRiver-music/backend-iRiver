from django.urls import path, include
from . import views

app_name = 'Discover'

urlpatterns = [
    path('edit',
         views.DiscoverEditView.as_view(), name='DiscoverEditView'),
    # last
    path('<str:uid>',
         views.discover, name='discover'),

]
