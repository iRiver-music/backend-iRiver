from django.test import TestCase

# self import
from .models import UserSocial,UserProfile,UserSettingEQ,UserSetting,UserMusicList

# Create your tests here.

def sqlconnecttest(useing=None):
    if useing!=None:
        row=UserSocial.objects.using(useing).all()
    else:
        row=UserSocial.objects.using("user").all()

    if len(row)>=0:
        return "pass"
    else:
        return "can't connect to sql!"