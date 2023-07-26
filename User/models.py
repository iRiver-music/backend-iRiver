import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# 國家清單
COUNTRY_CHOICES = (
    ("NN", "不透露"),
    ("US", "United States"),
    ("CA", "Canada"),
    ("JP", "Japan"),
    ("CN", "China"),
    ("TW", "Taiwan"),
    ("KR", "Korea"),
    ("SG", "Singapore"),
    ("MY", "Malaysia"),
    ("TH", "Thailand"),
    ("PH", "Philippines"),
    ("ID", "Indonesia"),
)
# 性別清單
GENDER = {
    ("U", "不透露"),
    ("M", "男"),
    ("F", "女"),
}


def custom_default_date():
    # Custom logic to set the default date and time
    return timezone.now()  # You can replace this with your own logic if needed


class Profile(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    email = models.CharField(max_length=24)
    username = models.CharField(max_length=24)
    phone = models.CharField(max_length=16)
    country = models.CharField(max_length=2, null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    user_img_url = models.CharField(max_length=255, null=True)
    level = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "profile"


class Setting(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    LANGUAGE = models.CharField(max_length=255)
    SHOW_MODAL = models.CharField(max_length=255)
    AUDIO_QUALITY = models.CharField(max_length=255)
    AUDIO_AUTO_PLAY = models.BooleanField()
    WIFI_AUTO_DOWNLOAD = models.BooleanField()
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "setting"


class EQ(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    ENGANCE_HIGH = models.BooleanField(null=True, blank=True)
    ENGANCE_MIDDLE = models.BooleanField(null=True, blank=True)
    ENGANCE_LOW = models.BooleanField(null=True, blank=True)
    ENGANCE_HEAVY = models.BooleanField(null=True, blank=True)
    STYLE = models.CharField(max_length=255, null=True, blank=True)
    EQ_HIGH = models.IntegerField(null=True)
    EQ_MIDDLE = models.IntegerField(null=True)
    EQ_LOW = models.IntegerField(null=True)
    EQ_HEAVY = models.IntegerField(null=True)
    EQ_DISTORTION = models.IntegerField(null=True)
    EQ_ZIP = models.IntegerField(null=True)
    SPATIAL_AUDIO = models.CharField(max_length=255, null=True, blank=True)
    _60HZ = models.IntegerField(null=True)
    _230HZ = models.IntegerField(null=True)
    _910HZ = models.IntegerField(null=True)
    _4kHZ = models.IntegerField(null=True)
    _14kHZ = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "eq"


class Social(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    email = models.CharField(max_length=24)
    uid = models.CharField(max_length=24)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "social"


class musicList(models.Model):
    playlist = models.CharField(max_length=255)
    music_ID = models.CharField(max_length=32)
    favorite = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
