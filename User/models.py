import uuid
import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
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
    phone = models.CharField(max_length=16, default=0)
    country = models.CharField(max_length=2, null=True, default=None)
    birthday = models.DateField(null=True, default=datetime.datetime.now)
    gender = models.CharField(max_length=1, null=True, default="K")
    level = models.PositiveSmallIntegerField(default=0, null=True)
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
    ENGANCE_HIGH = models.BooleanField(null=True, blank=True, default=False)
    ENGANCE_MIDDLE = models.BooleanField(null=True, blank=True, default=False)
    ENGANCE_LOW = models.BooleanField(null=True, blank=True, default=False)
    ENGANCE_HEAVY = models.BooleanField(null=True, blank=True, default=False)
    STYLE = models.CharField(max_length=255, null=True,
                             blank=True, default="auto")
    EQ_HIGH = models.IntegerField(null=True, default=0)
    EQ_MIDDLE = models.IntegerField(null=True, default=0)
    EQ_LOW = models.IntegerField(null=True, default=0)
    EQ_HEAVY = models.IntegerField(null=True, default=0)
    EQ_DISTORTION = models.IntegerField(null=True, default=0)
    EQ_ZIP = models.IntegerField(null=True, default=0)
    SPATIAL_AUDIO = models.CharField(
        max_length=255, null=True, blank=True, default="auto")
    _60HZ = models.IntegerField(null=True, default=0)
    _230HZ = models.IntegerField(null=True, default=0)
    _910HZ = models.IntegerField(null=True, default=0)
    _4kHZ = models.IntegerField(null=True, default=0)
    _14kHZ = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "eq"


class Social(models.Model):
    uid = models.CharField(max_length=36, primary_key=True)
    email = models.CharField(max_length=24)
    uid = models.CharField(max_length=24)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "social"
#


class Playlist(models.Model):
    uid = models.CharField(max_length=36, default='null')
    playlist = models.CharField(max_length=255)
    music_ID = models.CharField(max_length=32)
    favorite = models.PositiveSmallIntegerField(default=0)
    count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(default=custom_default_date)

    class Meta:
        app_label = "User"
        db_table = "playlist"


class ListeningHistory(models.Model):
    music_ID = models.CharField(max_length=200, unique=True)
    count = models.IntegerField(null=True)
    creat_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "User"
        db_table = "listeningHistory"

    def __str__(self):
        return f"{self.user} 在 {self.listening_time} 聽了 {self.song}"


class AdminCount(models.Model):
    # music
    artist = models.IntegerField()
    song = models.IntegerField()
    style = models.IntegerField()
    dow = models.IntegerField()

    # user
    user = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'User'
        db_table = 'Count'

    def __str__(self):
        return self.title
