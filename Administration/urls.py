from django.urls import path, include
from . import views
app_name = 'Administration'


urlpatterns = [
    #     serch

    path('info',
         views.info, name='info'),
]
